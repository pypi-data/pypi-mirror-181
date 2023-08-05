use std::fmt::Debug;
use std::num::{ParseFloatError, ParseIntError};
use std::ops::Deref;
use std::str::FromStr;

use nom::bytes::complete::take_until;
use nom::combinator::all_consuming;
use num_bigint::{BigInt, ParseBigIntError};
use nom_locate::{LocatedSpan, position};

use nom::{
    IResult, Parser, Err as NomError,
    branch::alt,
    bytes::complete::{escaped_transform, is_not, tag},
    character::complete::{alpha1, char, none_of, one_of, multispace0, space0},
    combinator::{map, map_res, opt, recognize, value, verify, success, peek},
    error::{ErrorKind, ParseError, FromExternalError, ContextError},
    multi::{many0, many1},
    sequence::{delimited, preceded, terminated, tuple, pair},
};

use crate::ast::*;
use crate::error::{Error, Location, Tagged, Syntax, SyntaxElement, Reason, Action};
use crate::object::{Object, Key};
use crate::traits::{Boxable, Taggable, Validatable};


type Span<'a> = LocatedSpan<&'a str>;

impl<'a> From<Span<'a>> for Location {
    fn from(x: Span<'a>) -> Self {
        Self {
            offset: x.location_offset(),
            line: x.location_line(),
            length: 0,
        }
    }
}


// Custom error type
#[derive(Debug)]
struct SyntaxError(Location, Option<Syntax>);

impl SyntaxError {
    fn to_error(self) -> Error {
        let SyntaxError(loc, reason) = self;
        Error {
            locations: Some(vec![(loc, Action::Parse)]),
            reason: reason.map(Reason::Syntax),
            rendered: None,
        }
    }
}


trait ExplainError<I> {
    fn error<'a, T>(loc: I, reason: T) -> Self where Syntax: From<T>;
}

impl<I> ExplainError<I> for SyntaxError where Location: From<I> {
    fn error<'a, T>(loc: I, reason: T) -> Self where Syntax: From<T> {
        Self(Location::from(loc), Some(Syntax::from(reason)))
    }
}

impl<'a> ParseError<Span<'a>> for SyntaxError {
    fn from_error_kind(loc: Span<'a>, _: ErrorKind) -> Self {
        Self(Location::from(loc), None)
    }

    fn from_char(loc: Span<'a>, _: char) -> Self {
        Self(Location::from(loc), None)
    }

    fn append(_: Span<'a>, _: ErrorKind, other: Self) -> Self {
        other
    }
}

impl<'a> ContextError<Span<'a>> for SyntaxError {
    fn add_context(_: Span<'a>, _: &'static str, other: Self) -> Self {
        other
    }
}

impl<'a> FromExternalError<Span<'a>, ParseIntError> for SyntaxError {
    fn from_external_error(loc: Span<'a>, _: ErrorKind, _: ParseIntError) -> Self {
        Self(Location::from(loc), None)
    }
}

impl<'a> FromExternalError<Span<'a>, ParseBigIntError> for SyntaxError {
    fn from_external_error(loc: Span<'a>, _: ErrorKind, _: ParseBigIntError) -> Self {
        Self(Location::from(loc), None)
    }
}

impl<'a> FromExternalError<Span<'a>, ParseFloatError> for SyntaxError {
    fn from_external_error(loc: Span<'a>, _: ErrorKind, _: ParseFloatError) -> Self {
        Self(Location::from(loc), None)
    }
}


fn literal<T>(x: T) -> Expr where Object: From<T> {
    Object::from(x).literal()
}


/// Convert a multiline string from source code to string by removing leading
/// whitespace from each line according to the rules for such strings.
fn multiline(s: &str) -> String {
    let mut lines = s.lines();

    let first = lines.next().unwrap().trim_start();

    let rest: Vec<&str> = lines.filter(|s: &&str| !s.deref().trim().is_empty()).collect();
    let indent =
        rest.iter()
            .filter(|s: &&&str| !s.trim().is_empty())
            .map(|s: &&str| s.deref().chars().take_while(|c| c.is_whitespace()).map(|_| 1).sum())
            .min().unwrap_or(0);

    let mut ret = first.to_string();
    for r in rest {
        if !ret.is_empty() {
            ret += "\n";
        }
        ret += &r.chars().skip(indent).collect::<String>();
    }

    ret
}


/// Temporary expression wrapper used for accurately tracking parenthesized
/// locations.
///
/// For parenthesized expressions, the Gold parser keeps track of both the outer
/// and the inner locations, whereas for non-parenthesized expressions, only the
/// inner location is tracked.
///
/// ```ignore
/// ( some_expression_here )
///   ^----- inner ------^
/// ^------- outer --------^
/// ```
///
/// In this way, when a parenthesized expression becomes a constituent part of
/// a larger expression, the parentheses can be included on both sides, by using
/// the outer span, e.g.:
///
/// ```ignore
/// ( 2 + 3 ) * 5
/// ^-----------^
/// ```
///
/// Instead of the confusing result that would result from using the inner span,
/// incorrectly giving the impression that imbalanced parentheses are allowed:
///
/// ```ignore
/// ( 2 + 3 ) * 5
///   ^---------^
/// ```
///
/// On the other hand, when a parenthesised expression is used in a context where
/// an error originates purely from the inner expression, Gold can disregard the
/// parentheses when reporting the error:
///
/// ```ignore
/// let x = ( some_function(y) ) in x + x
///           ^--------------^
/// ```
#[derive(Clone)]
enum Paren<T> {
    /// A naked (non-parenthesized) expression.
    Naked(Tagged<T>),

    /// A parenthesized expression with two layers of location tags: outer and inner.
    Parenthesized(Tagged<Tagged<T>>),
}


impl<T> Paren<T> {
    /// Return the inner expression with location tag, disregarding potential
    /// parentheses.
    fn inner(self) -> Tagged<T> {
        match self {
            Self::Naked(x) => x,
            Self::Parenthesized(x) => x.unwrap(),
        }
    }

    /// Return the outermost location span, either parenthesized or not.
    ///
    /// Use this when combining two spans.
    fn outer(&self) -> Location {
        match self {
            Self::Naked(x) => x.loc(),
            Self::Parenthesized(x) => x.loc(),
        }
    }

    fn wraptag<F, U>(self, f: F) -> Paren<U> where F: FnOnce(Tagged<T>) -> U {
        match self {
            Self::Naked(x) => Paren::<U>::Naked(x.wraptag(f)),
            Self::Parenthesized(x) => Paren::<U>::Parenthesized(x.map(|y| y.wraptag(f))),
        }
    }
}


type PExpr = Paren<Expr>;
type PList = Paren<ListElement>;
type PMap = Paren<MapElement>;


trait CompleteError<'a>:
    Debug +
    ExplainError<Span<'a>> +
    ParseError<Span<'a>> +
    ContextError<Span<'a>> +
    FromExternalError<Span<'a>, ParseIntError> +
    FromExternalError<Span<'a>, ParseBigIntError> +
    FromExternalError<Span<'a>, ParseFloatError> {}

impl<'a, T> CompleteError<'a> for T
where T:
    Debug +
    ExplainError<Span<'a>> +
    ParseError<Span<'a>> +
    ContextError<Span<'a>> +
    FromExternalError<Span<'a>, ParseIntError> +
    FromExternalError<Span<'a>, ParseBigIntError> +
    FromExternalError<Span<'a>, ParseFloatError> {}


type OpCons = fn(Tagged<Expr>, loc: Location) -> Operator;


/// Convert errors to failures.
fn fail<I, E: ParseError<I>, O, F, T>(
    mut parser: F,
    reason: T,
) -> impl FnMut(I) -> IResult<I, O, E>
where
    F: Parser<I, O, E>,
    I: nom::InputTake + nom::InputIter + Clone,
    E: ExplainError<I>,
    Syntax: From<T>,
    T: Copy
{
    move |input: I| {
        let (input, start) = position.parse(input)?;
        parser.parse(input).map_err(
            |err| match err {
                NomError::<E>::Failure(e) => NomError::Failure(e),
                NomError::<E>::Error(_) => {
                    NomError::Failure(<E as ExplainError<I>>::error(start, reason))
                },
                _ => err
            }
        )
    }
}


/// Apply a separator skip rule to an item parser. See [`seplist_opt_delim`] for
/// details.
fn apply_skip<I, E: ParseError<I>, O, F>(
    parser: F,
    skip_delimiter: bool,
) -> impl FnMut(I) -> IResult<I, (O, bool), E>
where
    F: Parser<I, O, E>,
{
    map(parser, move |x| (x, skip_delimiter))
}


/// Create an item parser that always skips the following separator. See
/// [`seplist_opt_delim`] for details.
fn do_skip<I, E: ParseError<I>, O, F>(
    parser: F,
) -> impl FnMut(I) -> IResult<I, (O, bool), E>
where
    F: Parser<I, O, E>,
{
    apply_skip(parser, true)
}


/// Create an item parser that never skips the following separator. See
/// [`seplist_opt_delim`] for details.
fn dont_skip<I, E: ParseError<I>, O, F>(
    parser: F,
) -> impl FnMut(I) -> IResult<I, (O, bool), E>
where
    F: Parser<I, O, E>,
{
    apply_skip(parser, false)
}


/// Separated list with delimiters and optional trailing separator.
///
/// The item parser should return a tuple with two items: the item itself, and a
/// boolean indicating whether the following separator should be skipped or not.
/// This is used in certain contexts, like map parsing.
fn seplist_opt_delim<Init, Item, Sep, Term, InitR, ItemR, SepR, TermR, I, E, T, U>(
    mut initializer: Init,
    mut item: Item,
    mut separator: Sep,
    mut terminator: Term,
    err_terminator_or_item: T,
    err_terminator_or_separator: U,
) -> impl FnMut(I) -> IResult<I, (InitR, Vec<ItemR>, TermR), E>
where
    Init: Parser<I, InitR, E>,
    Item: Parser<I, (ItemR, bool), E>,
    Sep: Parser<I, SepR, E>,
    Term: Parser<I, TermR, E>,
    I: Clone,
    E: ExplainError<I>,
    Syntax: From<T> + From<U>,
    T: Copy,
    U: Copy,
{
    move |mut i: I| {
        let (j, initr) = initializer.parse(i)?;
        i = j;

        let mut items = Vec::new();
        let mut expect_separator: bool;

        loop {

            // Try to parse an item
            match item.parse(i.clone()) {

                // Parsing item failed: we expect a terminator
                Err(NomError::Error(_)) => {
                    match terminator.parse(i.clone()) {
                        Err(NomError::Error(_)) => return Err(NomError::Failure(
                            <E as ExplainError<I>>::error(i, err_terminator_or_item)
                        )),
                        Err(e) => return Err(e),
                        Ok((i, termr)) => return Ok((i, (initr, items, termr))),
                    }
                }

                // Parsing item failed irrecoverably
                Err(e) => return Err(e),

                // Parsing item succeeded
                Ok((j, (it, skip_separator))) => {
                    i = j;
                    expect_separator = !skip_separator;
                    items.push(it);
                }
            }

            // If at this moment we don't expect a separator, try to parse a terminator
            if !expect_separator {
                match terminator.parse(i.clone()) {
                    Err(NomError::Error(_)) => { },
                    Err(e) => { return Err(e); },
                    Ok((i, termr)) => return Ok((i, (initr, items, termr))),
                }

                continue;
            }

            // Try to parse a separator
            match separator.parse(i.clone()) {

                // Parsing separator failed: we expect a terminator
                Err(NomError::Error(_)) => {
                    match terminator.parse(i.clone()) {
                        Err(NomError::Error(_)) => return Err(NomError::Failure(
                            <E as ExplainError<I>>::error(i, err_terminator_or_separator)
                        )),
                        Err(e) => return Err(e),
                        Ok((i, termr)) => return Ok((i, (initr, items, termr))),
                    }
                }

                // Parsing separator failed irrecoverably
                Err(e) => return Err(e),

                // Parsing separator succeeded
                Ok((j, _)) => { i = j; }
            }

        }

    }
}


/// Separated list with delimiters and optional trailing separator.
fn seplist<Init, Item, Sep, Term, InitR, ItemR, SepR, TermR, I, E, T, U>(
    initializer: Init,
    item: Item,
    separator: Sep,
    terminator: Term,
    err_terminator_or_item: T,
    err_terminator_or_separator: U,
) -> impl FnMut(I) -> IResult<I, (InitR, Vec<ItemR>, TermR), E>
where
    Init: Parser<I, InitR, E>,
    Item: Parser<I, ItemR, E>,
    Sep: Parser<I, SepR, E>,
    Term: Parser<I, TermR, E>,
    I: Clone,
    E: ExplainError<I>,
    Syntax: From<T> + From<U>,
    T: Copy,
    U: Copy,
{
    let item_parser = map(item, |it| (it, false));
    seplist_opt_delim(initializer, item_parser, separator, terminator, err_terminator_or_item, err_terminator_or_separator)
}


/// Wrap the output of a parser in Paren::Naked.
fn naked<I, E: ParseError<I>, F, U>(
    parser: F,
) -> impl FnMut(I) -> IResult<I, Paren<U>, E>
where
    F: Parser<I, Tagged<U>, E>,
{
    map(parser, Paren::<U>::Naked)
}


/// Consume whitespace after a parser.
///
/// Most parsers in this module should consume whitespace after, but not before.
fn postpad<I, O, E: ParseError<I>, F>(
    parser: F,
) -> impl FnMut(I) -> IResult<I, O, E>
where
    F: Parser<I, O, E>,
    I: Clone + nom::InputTakeAtPosition,
    <I as nom::InputTakeAtPosition>::Item: nom::AsChar + Clone,
{
    terminated(parser, multispace0)
}


/// Tag the output of a parser with a location.
///
/// Note that the inner parser should not consume whitespace after. Otherwise
/// the whitespace will be part of the tagged location. For that, use
/// [`positioned_postpad`].
fn positioned<I, O, E: ParseError<I>, F>(
    parser: F
) -> impl FnMut(I) -> IResult<I, Tagged<O>, E>
where
    F: Parser<I, O, E>,
    I: nom::InputTake + nom::InputIter + Clone,
    O: Taggable,
    Location: From<(I, I)>,
{
    map(
        tuple((position, parser, position)),
        |(l, o, r)| o.tag((l, r)),
    )
}


/// Tag the output of a parser with a location, and consume whitespace after.
///
/// This is the whitespace-aware version of [`positioned`].
fn positioned_postpad<I, O, E: ParseError<I>, F>(
    parser: F,
) -> impl FnMut(I) -> IResult<I, Tagged<O>, E>
where
    F: Parser<I, O, E>,
    I: nom::InputTakeAtPosition + nom::InputTake + nom::InputIter + Clone + nom::InputLength,
    <I as nom::InputTakeAtPosition>::Item: nom::AsChar + Clone,
    O: Taggable,
    Location: From<(I, I)>,
{
    postpad(positioned(parser))
}


/// Match a single named keyword. Unlike [`tag`] this does not match if the
/// keyword is a prefix of some other name or identifier.
fn keyword<'a, E: ParseError<Span<'a>>>(
    value: &'a str,
) -> impl FnMut(Span<'a>) -> IResult<Span<'a>, Span<'a>, E> {
    verify(
        is_not("=,;.:-+/*[](){}|\"\' \t\n\r"),
        move |out: &Span<'a>| { *out.fragment() == value },
    )
}


/// List of keywords that must be avoided by the [`identifier`] parser.
static KEYWORDS: [&'static str; 15] = [
    "for",
    "when",
    "if",
    "then",
    "else",
    "let",
    "in",
    "true",
    "false",
    "null",
    "and",
    "or",
    "not",
    "as",
    "import",
];


/// Match an identfier.
///
/// This parser will refuse to match known keywords (see [`KEYWORDS`]).
fn identifier<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Key>, E> {
    positioned(map(
        verify(
            recognize(pair(
                alt((alpha1::<Span<'a>, E>, tag("_"))),
                opt(is_not("=.,:;-+/*[](){}^|\"\' \t\n\r")),
            )),
            |out: &Span<'a>| !KEYWORDS.contains(out.fragment()),
        ),
        |x| Key::new(*x.fragment()),
    ))(input)
}


/// Match an identifier in a map context.
///
/// Maps have relaxed conditions on identifier names compared to 'regular' code.
fn map_identifier<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Key>, E> {
    map(
        positioned(is_not(",=:$}()|\"\' \t\n\r")),
        |x| x.map(|x: Span<'a>| Key::new(x.fragment()))
    )(input)
}


/// Match a decimal: a sequence of digits 0-9, optionally interspersed with
/// underscores.
fn decimal<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, &'a str, E> {
    map(
        recognize(tuple((
            one_of("0123456789"),
            many0(one_of("0123456789_")),
        ))),
        |x: Span<'a>| *x.fragment(),
    )(input)
}


/// Match an exponent: an e or E followed by an optional sign and a decimal.
fn exponent<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, &str, E> {
    map(
        recognize(tuple((
            one_of("eE"),
            opt(one_of("+-")),
            decimal,
        ))),
        |x: Span<'a>| *x.fragment(),
    )(input)
}


/// Match a literal integer expression in decimal form.
fn integer<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(map_res(
        decimal,

        |x| {
            let s = x.replace("_", "");
            i64::from_str(s.as_ref()).map_or_else(
                |_| BigInt::from_str(s.as_ref()).map(literal),
                |x| Ok(literal(x)),
            )
        },
    )))(input)
}


/// Match a literal floating-point number expression in decimal form.
fn float<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(map_res(
        // Three forms of floating point numbers. We match only the string here,
        // relying on built-in Rust float parsing to extract the actual number.
        alt((

            // Decimal integer followed by dot, and potentially fractional part and exponent.
            recognize(tuple((
                decimal,
                char('.'),
                opt(decimal),
                opt(exponent),
            ))),

            // Dot followed by decimal fractional part.
            recognize(tuple((
                char('.'),
                decimal,
                opt(exponent),
            ))),

            // Pure integer followed by exponent.
            recognize(tuple((
                decimal,
                exponent,
            ))),

        )),

        |out: Span<'a>| out.fragment().deref().replace("_", "").parse::<f64>().map(literal)
    )))(input)
}


/// Matches a raw string part.
///
/// This means all characters up to a terminating symbol: either a closing quote
/// or a dollar sign, signifying the beginning of an interpolated segment. This
/// parser does *not* parse the initial quote or the terminating symbol,
/// whatever that may be.
fn raw_string<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, String, E> {
    verify(
        escaped_transform(
            recognize(many1(none_of("\"\\$\n"))),
            '\\',
            alt((
                value("\"", tag("\"")),
                value("\\", tag("\\")),
                value("$", tag("$")),
            )),
        ),
        |x: &str| { x.len() > 0 },
    )(input)
}


/// Matches a non-interpolated string element.
///
/// This is just the output of [`raw_string`] returned as a [`StringElement`].
fn string_data<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, StringElement, E> {
    map(
        raw_string,
        StringElement::raw
    )(input)
}


/// Matches an interpolated string element.
fn string_interp<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, StringElement, E> {
    map(
        delimited(
            terminated(
                char('$'),
                fail(postpad(char('{')), SyntaxElement::OpenBrace),
            ),
            fail(expression, SyntaxElement::Expression),
            fail(char('}'), SyntaxElement::CloseBrace),
        ),

        |x| StringElement::Interpolate(x.inner()),
    )(input)
}


/// Matches a string part.
///
/// This parser matches an opening quote, followed by a sequence of string
/// elements: either raw string data or interpolated expressions, followed by a
/// closing quote.
fn string_part<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Vec<StringElement>, E> {
    delimited(
        char('\"'),
        many0(alt((string_interp, string_data))),
        fail(char('\"'), SyntaxElement::DoubleQuote),
    )(input)
}


/// Matches a string.
///
/// This consists of a sequence of one or more string parts, separated by
/// whitespace.
fn string<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(map(
        many1(positioned_postpad(string_part)),
        |x| {
            let start = x.first().unwrap().loc();
            let end = x.last().unwrap().loc();
            Expr::string(x.into_iter().map(Tagged::unwrap).flatten().collect()).tag((start, end))
        }
    ))(input)
}


/// Matches a boolean literal.
fn boolean<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(alt((
        value(literal(true), keyword("true")),
        value(literal(false), keyword("false")),
    ))))(input)
}


/// Matches a null literal.
fn null<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(
        value(Object::Null.literal(), keyword("null"))
    ))(input)
}


/// Matches any atomic (non-divisible) expression.
///
/// Although strings are technically not atomic due to possibly interpolated
/// expressions.
fn atomic<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    alt((
        null,
        boolean,
        float,
        integer,
        string,
    ))(input)
}


/// Matches a list element: anything that is legal in a list.
///
/// There are four cases:
/// - singleton elements: `[2]`
/// - splatted iterables: `[...x]`
/// - conditional elements: `[if cond: @]`
/// - iterated elements: `[for x in y: @]`
fn list_element<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PList, E> {
    alt((

        // Splat
        naked(map(
            tuple((
                positioned(postpad(tag("..."))),
                fail(expression, SyntaxElement::Expression),
            )),
            |(start, expr)| {
                let loc = Location::from((&start, expr.outer()));
                ListElement::Splat(expr.inner()).tag(loc)
            },
        )),

        // Iteration
        naked(map(
            tuple((
                positioned_postpad(keyword("for")),
                fail(binding, SyntaxElement::Binding),
                preceded(
                    fail(postpad(keyword("in")), SyntaxElement::In),
                    fail(expression, SyntaxElement::Expression),
                ),
                preceded(
                    fail(postpad(char(':')), SyntaxElement::Colon),
                    fail(list_element, SyntaxElement::ListElement)
                ),
            )),
            |(start, binding, iterable, expr)| {
                let loc = Location::from((&start, expr.outer()));
                ListElement::Loop {
                    binding,
                    iterable: iterable.inner(),
                    element: Box::new(expr.inner()),
                }.tag(loc)
            }
        )),

        // Conditional
        naked(map(
            tuple((
                positioned_postpad(keyword("when")),
                fail(expression, SyntaxElement::Expression),
                preceded(
                    fail(postpad(char(':')), SyntaxElement::Colon),
                    fail(list_element, SyntaxElement::ListElement),
                ),
            )),
            |(start, condition, expr)| {
                let loc = Location::from((&start, expr.outer()));
                ListElement::Cond {
                    condition: condition.inner(),
                    element: Box::new(expr.inner()),
                }.tag(loc)
            },
        )),

        // Singleton
        map(expression, |x| x.wraptag(ListElement::Singleton))

    ))(input)
}


/// Matches a list.
///
/// A list is composed of an opening bracket, a potentially empty
/// comma-separated list of list elements, an optional terminal comma and a
/// closing bracket.
fn list<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(map(
        seplist(
            postpad(char('[')),
            list_element,
            postpad(char(',')),
            char(']'),
            (SyntaxElement::CloseBracket, SyntaxElement::ListElement),
            (SyntaxElement::CloseBracket, SyntaxElement::Comma),
        ),

        |(_, x, _)| Expr::List(x.into_iter().map(|y| y.inner()).collect()),
    )))(input)
}


/// Matches a singleton key in a map context.
///
/// This is either a dollar sign followed by an expression, a string literal or
/// a pure map identifier.
fn map_key_singleton<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, (Span<'a>, PExpr), E> {
    tuple((
        position,
        alt((
            naked(map(
                preceded(
                    postpad(char('$')),
                    fail(expression, SyntaxElement::Expression),
                ),
                PExpr::inner,
            )),

            postpad(string),

            naked(map(
                postpad(map_identifier),
                |key| key.map(Object::from).map(Expr::Literal),
            )),
        ))
    ))(input)
}


/// Matches a line with indentation of at least `col` spaces.
///
/// This does not return the line itself as a result, but the input at the
/// beginning of the next line.
fn line_indent_at_least<'a>(
    col: usize,
    input: Span<'a>,
) -> IResult<Span<'a>, Span<'a>, ()> {
    let (input, _) = space0(input)?;
    let (input, pos) = position(input)?;
    let this_col = pos.get_column();
    if this_col > col {
        let (input, _) = take_until("\n")(input)?;
        let (input, _) = tag("\n")(input)?;
        Ok((input, input))
    } else {
        Err(NomError::Error(()))
    }
}


/// Matches a singleton value in a map context.
///
/// This is either a double comma followed by a multiline string, or a single
/// comma followed by an expression.
fn map_value_singleton<'a, E: CompleteError<'a>>(
    col: usize,
    input: Span<'a>,
) -> IResult<Span<'a>, (PExpr, bool), E> {
    alt((
        do_skip(naked(map(
            preceded(
                tag("::"),
                positioned_postpad(recognize(|i: Span<'a>| {
                    let (mut i, _) = take_until("\n")(i)?;
                    loop {
                        match peek(|j| line_indent_at_least(col, j))(i) {
                            Ok((_, input)) => {
                                i = input;
                            },
                            Err(_) => {
                                break;
                            },
                        }
                    }
                    Ok((i, ()))
                })),
            ),
            |s| s.map(|s| Expr::string(vec![StringElement::raw(multiline(s.as_ref()))])),
        ))),

        dont_skip(preceded(
            fail(postpad(char(':')), SyntaxElement::Colon),
            fail(expression, SyntaxElement::Expression),
        )),
    ))(input)
}


/// Matches a singleton map element: a singleton key followed by a singleton
/// value.
fn map_element_singleton<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, (PMap, bool), E> {
    let (input, (span, key)) = map_key_singleton(input)?;
    let col = span.get_column();

    let (input, (value, skip_sep)) = map_value_singleton(col, input)?;

    let loc = Location::from((span, value.outer()));
    let ret = MapElement::Singleton { key: key.inner(), value: value.inner() }.tag(loc);

    Ok((input, (PMap::Naked(ret), skip_sep)))
}


/// Matches a map element: anything that is legal in a map.
///
/// There are five cases:
/// - singleton elements
/// - splatted iterables: `{...x}`
/// - conditional elements: `{if cond: @}`
/// - iterated elements: `{for x in y: @}`
fn map_element<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, (PMap, bool), E> {
    alt((

        // Splat
        dont_skip(naked(map(
            tuple((
                positioned_postpad(tag("...")),
                fail(expression, SyntaxElement::Expression),
            )),
            |(start, expr)| {
                let loc = Location::from((&start, expr.outer()));
                MapElement::Splat(expr.inner()).tag(loc)
            },
        ))),

        // Iteration
        map(
            tuple((
                positioned_postpad(keyword("for")),
                fail(binding, SyntaxElement::Binding),
                preceded(
                    fail(postpad(keyword("in")), SyntaxElement::In),
                    fail(expression, SyntaxElement::Expression),
                ),
                preceded(
                    fail(postpad(char(':')), SyntaxElement::Colon),
                    fail(map_element, SyntaxElement::MapElement),
                ),
            )),
            |(start, binding, iterable, (expr, skip))| {
                let loc = Location::from((&start, expr.outer()));
                let ret = MapElement::Loop {
                    binding,
                    iterable: iterable.inner(),
                    element: Box::new(expr.inner()),
                }.tag(loc);
                (PMap::Naked(ret), skip)
            },
        ),

        // Conditional
        map(
            tuple((
                positioned_postpad(keyword("when")),
                fail(expression, SyntaxElement::Expression),
                preceded(
                    fail(postpad(char(':')), SyntaxElement::Colon),
                    fail(map_element, SyntaxElement::MapElement),
                ),
            )),
            |(start, condition, (expr, skip))| {
                let loc = Location::from((&start, expr.outer()));
                let ret = MapElement::Cond {
                    condition: condition.inner(),
                    element: Box::new(expr.inner())
                }.tag(loc);
                (PMap::Naked(ret), skip)
            },
        ),

        // Various types of singletons
        map_element_singleton,

    ))(input)
}



/// Matches a map.
///
/// A list is composed of an opening brace, a potentially empty comma-separated
/// list of map elements, an optional terminal comma and a closing brace.
fn mapping<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    naked(positioned(map(
        seplist_opt_delim(
            postpad(char('{')),
            map_element,
            postpad(char(',')),
            char('}'),
            (SyntaxElement::CloseBrace, SyntaxElement::MapElement),
            (SyntaxElement::CloseBrace, SyntaxElement::Comma),
        ),

        |(_, x, _)| Expr::Map(x.into_iter().map(|y| y.inner()).collect()),
    )))(input)
}


/// Matches a parenthesized expression.
///
/// This is the only possible source of Paren::Parenthesized in the Gold
/// language. All other parenthesized variants stem from this origin.
fn paren<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    map(
        tuple((
            positioned_postpad(char('(')),
            fail(expression, SyntaxElement::Expression),
            fail(positioned_postpad(char(')')), SyntaxElement::CloseParen),
        )),

        |(start, expr, end)| {
            let loc = Location::from((&start, &end));
            PExpr::Parenthesized(expr.inner().tag(loc))
        }
    )(input)
}


/// Matches an expression that can be an operand.
///
/// The tightest binding operators are the postfix operators, so this class of
/// expressions are called 'postixable' expressions. Only expressions with a
/// well defined end are postfixable: in particular, functions, let-blocks and
/// tertiary expressions are not postfixable, but parenthesized expressions are.
fn postfixable<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    postpad(alt((
        paren,
        atomic,
        naked(positioned(map(identifier, Expr::Identifier))),
        list,
        mapping,
    )))(input)
}


/// Matches a dot-syntax subscripting operator.
///
/// This is a dot followed by an identifier.
fn object_access<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Operator>, E> {
    map(
        tuple((
            positioned_postpad(char('.')),
            fail(identifier, SyntaxElement::Identifier),
        )),
        |(dot, out)| Operator::BinOp(
            BinOp::Index.tag(&dot),
            out.map(Object::IntString).map(Expr::Literal).to_box(),
        ).tag((&dot, &out)),
    )(input)
}


/// Matches a bracket-syntax subscripting operator.
///
/// This is an open bracket followed by any expression and a closing bracket.
fn object_index<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Operator>, E> {
    map(
        tuple((
            positioned_postpad(char('[')),
            fail(expression, SyntaxElement::Expression),
            fail(positioned(char(']')), SyntaxElement::CloseBracket),
        )),
        |(a, expr, b)| Operator::BinOp(BinOp::Index.tag((&a, &b)), expr.inner().to_box()).tag((&a, &b)),
    )(input)
}


/// Matches a function argument element.
///
/// There are three cases:
/// - splatted iterables: `f(...x)`
/// - keyword arguments: `f(x: y)`
/// - singleton arguments: `f(x)`
fn function_arg<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<ArgElement>, E> {
    alt((

        // Splat
        map(
            tuple((
                positioned_postpad(tag("...")),
                fail(expression, SyntaxElement::Expression),
            )),
            |(x, y)| {
                let rloc = y.outer();
                ArgElement::Splat(y.inner()).tag((&x, rloc))
            },
        ),

        // Keyword
        map(
            tuple((
                postpad(identifier),
                preceded(
                    postpad(char(':')),
                    fail(expression, SyntaxElement::Expression),
                ),
            )),
            |(name, expr)| {
                let loc = Location::from((&name, expr.outer()));
                ArgElement::Keyword(name, expr.inner()).tag(loc)
            },
        ),

        // Singleton
        map(
            expression,
            |x| {
                let loc = x.outer();
                ArgElement::Singleton(x.inner()).tag(loc)
            },
        ),

    ))(input)
}


/// Matches a function call operator.
///
/// This is an open parenthesis followed by a possibly empty list of
/// comma-separated argument elements, followed by an optional comma and a
/// closin parenthesis.
fn function_call<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Operator>, E> {
    map(
        seplist(
            positioned_postpad(char('(')),
            function_arg,
            postpad(char(',')),
            positioned_postpad(char(')')),
            (SyntaxElement::CloseParen, SyntaxElement::ArgElement),
            (SyntaxElement::CloseParen, SyntaxElement::Comma),
        ),
        |(a, expr, b)| Operator::FunCall(expr.tag((&a, &b))).tag((&a, &b)),
    )(input)
}


/// Matches any postfix operator expression.
///
/// This is a postfixable expression (see [`postfixable`]) followed by an
/// arbitrary sequence of postfix operators.
fn postfixed<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    map(
        tuple((
            postfixable,
            many0(postpad(alt((
                object_access,
                object_index,
                function_call,
            )))),
        )),

        |(expr, ops)| {
            ops.into_iter().fold(
                expr,
                |expr, operator| {
                    let loc = Location::from((expr.outer(), &operator));
                    PExpr::Naked(Expr::Operator {
                        operand: Box::new(expr.inner()),
                        operator: operator.unwrap()
                    }.tag(loc))
                },
            )
        },
    )(input)
}


/// Matches any prefixed operator expression.
///
/// This is an arbitrary sequence of prefix operators followed by a postfixed
/// expression.
fn prefixed<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    alt((
        power,

        map(
            tuple((
                many1(alt((
                    map(positioned_postpad(tag("+")), |x| x.map(|_| UnOp::Passthrough)),
                    map(positioned_postpad(tag("-")), |x| x.map(|_| UnOp::ArithmeticalNegate)),
                    map(positioned_postpad(keyword("not")), |x| x.map(|_| UnOp::LogicalNegate)),
                ))),
                fail(power, SyntaxElement::Operand),
            )),

            |(ops, expr)| {
                ops.into_iter().rev().fold(
                    expr,
                    |expr, operator| {
                        let loc = Location::from((&operator, expr.outer()));
                        PExpr::Naked(Expr::Operator {
                            operand: Box::new(expr.inner()),
                            operator: Operator::UnOp(operator)
                        }.tag(loc))
                    },
                )
            },
        )
    ))(input)
}


/// Utility parser for parsing a single binary operator with operand.
///
/// `operators` should return, loosely, a function Expr -> Operator.
/// `operand` should return an Expr.
///
/// The result, essentially, is the result of `operators` applied to the result
/// of `operand`, thus, an Operator.
///
/// Note that in the Gold abstract syntax tree model, an operator is anything
/// that 'acts' on an expression. In this interpretation, in an expression such
/// as `1 + 2`, `+ 2` is the operator that acts on `1`.
fn binop<I, E: ParseError<I>, G, H>(
    operators: G,
    operand: H,
) -> impl FnMut(I) -> IResult<I, Tagged<Operator>, E>
where
    I: Clone + nom::InputTakeAtPosition + nom::InputTake + nom::InputIter + nom::InputLength,
    <I as nom::InputTakeAtPosition>::Item: nom::AsChar + Clone,
    G: Parser<I, OpCons, E>,
    H: Parser<I, PExpr, E>,
    E: ExplainError<I>,
    Location: From<(I, I)>,
{
    map(
        tuple((
            positioned_postpad(operators),
            fail(operand, SyntaxElement::Operand),
        )),
        |(func, expr)| {
            let loc = Location::span(func.loc(), expr.outer());
            func.as_ref()(expr.inner(), func.loc()).direct_tag(loc)
        },
    )
}


/// Utility parser for parsing a left- or right-associative sequence of operators.
///
/// `operators` is normally a parser created by [`binop`], that is, something
/// that returns an `Operator`.
fn binops<I, E: ParseError<I>, G, H>(
    operators: G,
    operand: H,
    right: bool,
) -> impl FnMut(I) -> IResult<I, PExpr, E>
where
    I: Clone + nom::InputTakeAtPosition + nom::InputLength,
    <I as nom::InputTakeAtPosition>::Item: nom::AsChar + Clone,
    E: ExplainError<I>,
    G: Parser<I, Tagged<Operator>, E>,
    H: Parser<I, PExpr, E> + Copy,
{
    map(
        tuple((
            operand,
            many0(operators),
        )),
        move |(expr, ops)| {
            let acc = |expr: PExpr, operator: Tagged<Operator>| {
                let loc = Location::from((expr.outer(), &operator));
                PExpr::Naked(Expr::Operator {
                    operand: Box::new(expr.inner()),
                    operator: operator.unwrap(),
                }.tag(loc))
            };
            if right {
                ops.into_iter().rev().fold(expr, acc)
            } else {
                ops.into_iter().fold(expr, acc)
            }
        },
    )
}


/// Matches the exponentiation precedence level.
///
/// The exponentiation operator, unlike practically every other operator, is
/// right-associative, and asymmetric in its operands: it binds tighter than
/// prefix operators on the left, but not on the right.
fn power<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    binops(
        binop(
            alt((
                value(Operator::power as OpCons, tag("^")),
            )),
            prefixed,
        ),
        postfixed,
        true,
    )(input)
}


/// Utility parser for matching a sequence of left-associative operators with
/// symmetric operands. In other words, most conventional operators.
fn lbinop<I, E: ParseError<I>, G, H>(
    operators: G,
    operands: H
) -> impl FnMut(I) -> IResult<I, PExpr, E>
where
    I: Clone + nom::InputTakeAtPosition + nom::InputLength + nom::InputTake + nom::InputIter,
    <I as nom::InputTakeAtPosition>::Item: nom::AsChar + Clone,
    G: Parser<I, OpCons, E>,
    H: Parser<I, PExpr, E> + Copy,
    E: ExplainError<I>,
    Location: From<(I, I)>,
{
    binops(binop(operators, operands), operands, false)
}


/// Matches the multiplication precedence level.
fn product<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::multiply as OpCons, tag("*")),
            value(Operator::integer_divide as OpCons, tag("//")),
            value(Operator::divide as OpCons, tag("/")),
        )),
        prefixed,
    )(input)
}


/// Matches the addition predecence level.
fn sum<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::add as OpCons, tag("+")),
            value(Operator::subtract as OpCons, tag("-")),
        )),
        product,
    )(input)
}


/// Matches the inequality comparison precedence level.
fn inequality<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::less_equal as OpCons, tag("<=")),
            value(Operator::greater_equal as OpCons, tag(">=")),
            value(Operator::less as OpCons, tag("<")),
            value(Operator::greater as OpCons, tag(">")),
        )),
        sum,
    )(input)
}


/// Matches the equality comparison precedence level.
fn equality<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::equal as OpCons, tag("==")),
            value(Operator::not_equal as OpCons, tag("!=")),
        )),
        inequality,
    )(input)
}


/// Matches the conjunction ('and') precedence level.
fn conjunction<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::and as OpCons, tag("and")),
        )),
        equality,
    )(input)
}


/// Matches the disjunction ('or') precedence level.
fn disjunction<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    lbinop(
        alt((
            value(Operator::or as OpCons, tag("or")),
        )),
        conjunction,
    )(input)
}


/// Matches an identifier binding. This is essentially the same as a normal
/// identifier.
fn ident_binding<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Binding>, E> {
    postpad(alt((
        map(
            positioned(identifier),
            |out| out.map(Binding::Identifier),
        ),
    )))(input)
}


/// Matches a list binding element: anything that's legal in a list unpacking
/// environment.
///
/// There are four cases:
/// - anonymous slurp: `let [...] = x`
/// - named slurp: `let [...y] = x`
/// - singleton binding: `let [y] = x`
/// - singleton binding with default: `let [y = z] = x`
fn list_binding_element<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<ListBindingElement>, E> {
    alt((

        // Named and anonymous slurps
        positioned(map(
            preceded(
                tag("..."),
                opt(identifier)
            ),
            |ident| ident.map(ListBindingElement::SlurpTo).unwrap_or(ListBindingElement::Slurp),
        )),

        // Singleton bindings with or without defaults
        map(
            tuple((
                binding,
                opt(preceded(
                    postpad(char('=')),
                    fail(expression, SyntaxElement::Expression),
                )),
            )),

            |(b, e)| {
                let loc = if let Some(d) = &e {
                    Location::from((&b, d.outer()))
                } else {
                    b.loc()
                };

                ListBindingElement::Binding {
                    binding: b,
                    default: e.map(PExpr::inner)
                }.tag(loc)
            },
        ),

    ))(input)
}


/// Matches a list binding.
///
/// This is a comma-separated list of list binding elements, optionally
/// terminated by a comma.
fn list_binding<'a, E: CompleteError<'a>, T, U, V>(
    initializer: impl Parser<Span<'a>, V, E> + Copy,
    terminator: impl Parser<Span<'a>, V, E> + Copy,
    err_terminator_or_item: T,
    err_terminator_or_separator: U,
) -> impl FnMut(Span<'a>) -> IResult<Span<'a>, (Tagged<ListBinding>, V), E>
where
    Syntax: From<T> + From<U>,
    T: Copy,
    U: Copy,
{
    move |input: Span<'a>| map(
        seplist(
            positioned_postpad(initializer),
            list_binding_element,
            postpad(char(',')),
            positioned_postpad(terminator),
            err_terminator_or_item,
            err_terminator_or_separator,
        ),
        |(a, x, b)| (ListBinding(x).tag((&a, &b)), b.unwrap()),
    )(input)
}


/// Matches a map binding element: anything that's legal in a map unpacking environment.
///
/// There are five cases:
/// - named slurp: `let {...y} = x`
/// - singleton binding: `let {y} = x`
/// - singleton binding with unpacking: `let {y as z} = x`
/// - singleton binding with default: `let {y = z} = x`
/// - singleton binding with unpacking and default: `let {y as z = q} = x`
fn map_binding_element<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<MapBindingElement>, E> {
    alt((

        // Slurp
        positioned(map(
            preceded(
                tag("..."),
                fail(identifier, SyntaxElement::Identifier),
            ),
            |i| MapBindingElement::SlurpTo(i),
        )),

        // All variants of singleton bindings
        map(
            tuple((
                alt((

                    // With unpacking
                    map(
                        tuple((
                            postpad(map_identifier),
                            preceded(
                                postpad(tag("as")),
                                fail(binding, SyntaxElement::Binding),
                            ),
                        )),
                        |(name, binding)| (name, Some(binding)),
                    ),

                    // Without unpacking
                    map(
                        postpad(map_identifier),
                        |name| (name, None),
                    ),

                )),

                // Optional default
                opt(
                    preceded(
                        postpad(char('=')),
                        fail(expression, SyntaxElement::Expression),
                    ),
                ),
            )),

            |((name, binding), default)| {
                let mut loc = name.loc();
                if let Some(b) = &binding { loc = Location::from((loc, b.loc())); };
                if let Some(d) = &default { loc = Location::from((loc, d.outer())); };
                let rval = match binding {
                    None => MapBindingElement::Binding {
                        key: name,
                        binding: Binding::Identifier(name).tag(&name),
                        default: default.map(PExpr::inner),
                    },
                    Some(binding) => MapBindingElement::Binding {
                        key: name,
                        binding,
                        default: default.map(PExpr::inner),
                    },
                };
                rval.tag(loc)
            },
        ),
    ))(input)
}


/// Matches a map binding.
///
/// This is a comma-separated list of list binding elements, optionally
/// terminated by a comma.
fn map_binding<'a, E: CompleteError<'a>, T, U, V>(
    initializer: impl Parser<Span<'a>, V, E> + Copy,
    terminator: impl Parser<Span<'a>, V, E> + Copy,
    err_terminator_or_item: T,
    err_terminator_or_separator: U,
) -> impl FnMut(Span<'a>) -> IResult<Span<'a>, Tagged<MapBinding>, E>
where
    Syntax: From<T> + From<U>,
    T: Copy,
    U: Copy,
{
    move |input: Span<'a>| map(
        seplist(
            positioned_postpad(initializer),
            map_binding_element,
            postpad(char(',')),
            positioned_postpad(terminator),
            err_terminator_or_item,
            err_terminator_or_separator,
        ),
        |(a, x, b)| MapBinding(x).tag((&a, &b)),
    )(input)
}


/// Matches a binding.
///
/// There are three cases:
/// - An identifier binding (leaf node)
/// - A list binding
/// - A map binding
fn binding<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, Tagged<Binding>, E> {
    alt((
        ident_binding,

        // TODO: Do we need double up location tagging here?
        postpad(
            map(
                list_binding(
                    |i| char('[')(i),
                    |i| char(']')(i),
                    (SyntaxElement::CloseBracket, SyntaxElement::ListBindingElement),
                    (SyntaxElement::CloseBracket, SyntaxElement::Comma),
                ),
                |(x,_)| {
                    let loc = x.loc();
                    x.wrap(Binding::List, loc)
                },
            )
        ),

        // TODO: Do we need double up location tagging here?
        postpad(
            map(
                map_binding(
                    |i| char('{')(i),
                    |i| char('}')(i),
                    (SyntaxElement::CloseBrace, SyntaxElement::MapBindingElement),
                    (SyntaxElement::CloseBrace, SyntaxElement::Comma),
                ),
                |x| {
                    let loc = x.loc();
                    x.wrap(Binding::Map, loc)
                },
            )
        ),
    ))(input)
}


/// Matches a standard function definition.
///
/// This is the 'fn' keyword followed by a list binding and an optional map
/// binding, each with slightly different delimiters from conventional
/// let-binding syntax. It is concluded by a double arrow (=>) and an
/// expression.
fn normal_function<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    let (i, (args, end)) = list_binding(
        |i| char('|')(i),
        |i| alt((char('|'), char(';')))(i),
        (SyntaxElement::Pipe, SyntaxElement::Semicolon, SyntaxElement::PosParam),
        (SyntaxElement::Pipe, SyntaxElement::Semicolon, SyntaxElement::Comma),
    )(input)?;

    let (j, kwargs) = if end == ';' {
        let (j, kwargs) = map_binding(
            |i| success(' ')(i),
            |i| char('|')(i),
            (SyntaxElement::Pipe, SyntaxElement::KeywordParam),
            (SyntaxElement::Pipe, SyntaxElement::Comma),
        )(i)?;
        (j, Some(kwargs))
    } else {
        (i, None)
    };

    let (l, expr) = fail(expression, SyntaxElement::Expression)(j)?;
    let loc = Location::from((args.loc(), expr.outer()));

    let result = PExpr::Naked(Expr::Function {
        positional: args.unwrap(),
        keywords: kwargs.map(Tagged::unwrap),
        expression: expr.inner().to_box(),
    }.tag(loc));

    Ok((l, result))
}


/// Matches a keyword-only function.
///
/// This is a conventional map binding followed by a double arrow (=>) and an
/// expression.
fn keyword_function<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    map(
        tuple((
            postpad(map_binding(
                |i| tag("{|")(i),
                |i| tag("|}")(i),
                (SyntaxElement::CloseCurlyPipe, SyntaxElement::KeywordParam),
                (SyntaxElement::CloseCurlyPipe, SyntaxElement::Comma),
            )),
            fail(expression, SyntaxElement::Expression),
        )),

        |(kwargs, expr)| {
            let loc = Location::from((&kwargs, expr.outer()));
            PExpr::Naked(Expr::Function {
                positional: ListBinding(vec![]),
                keywords: Some(kwargs.unwrap()),
                expression: Box::new(expr.inner()),
            }.tag(loc))
        },
    )(input)
}


/// Matches a function.
///
/// The heavy lifting of this function is done by [`normal_function`] or
/// [`keyword_function`].
fn function<'a, E: CompleteError<'a>>(
    input: Span<'a>
) -> IResult<Span<'a>, PExpr, E>
where
    E: ExplainError<Span<'a>>
{
    alt((
        keyword_function,
        normal_function,
    ))(input)
}


/// Matches a let-binding block.
///
/// This is an arbitrary (non-empty) sequence of let-bindings followed by the
/// keyword 'in' and then an expression.
///
/// A let-binding consists of the keyword 'let' followed by a binding, an equals
/// symbol and an expression.
fn let_block<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    map(
        tuple((
            position,
            many1(
                tuple((
                    preceded(
                        postpad(keyword("let")),
                        fail(binding, SyntaxElement::Binding),
                    ),
                    preceded(
                        fail(postpad(tag("=")), SyntaxElement::Equals),
                        fail(expression, SyntaxElement::Expression),
                    ),
                )),
            ),
            preceded(
                fail(postpad(tag("in")), SyntaxElement::In),
                fail(expression, SyntaxElement::Expression),
            ),
        )),
        |(start, bindings, expr)| {
            let loc = Location::from((start, expr.outer()));
            PExpr::Naked(Expr::Let {
                bindings: bindings.into_iter().map(|(x,y)| (x,y.inner())).collect(),
                expression: Box::new(expr.inner())
            }.tag(loc))
        },
    )(input)
}


/// Matches a branching expression (tertiary operator).
///
/// This consists of the keywords 'if', 'then' and 'else', each followed by an
/// expression.
fn branch<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    map(
        tuple((
            positioned_postpad(keyword("if")),
            fail(expression, SyntaxElement::Expression),
            preceded(
                fail(postpad(keyword("then")), SyntaxElement::Then),
                fail(expression, SyntaxElement::Expression),
            ),
            preceded(
                fail(postpad(keyword("else")), SyntaxElement::Else),
                fail(expression, SyntaxElement::Expression),
            ),
        )),

        |(start, condition, true_branch, false_branch)| {
            let loc = Location::from((&start, false_branch.outer()));
            PExpr::Naked(Expr::Branch {
                condition: Box::new(condition.inner()),
                true_branch: Box::new(true_branch.inner()),
                false_branch: Box::new(false_branch.inner()),
            }.tag(loc))
        },
    )(input)
}


/// Matches a composite expression.
///
/// This is a catch-all terms for special expressions that do not participate in
/// the operator sequence: let blocks, branches, and functions.
fn composite<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    alt((
        let_block,
        branch,
        function,
    ))(input)
}


/// Matches any expression.
fn expression<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, PExpr, E> {
    alt((
        composite,
        disjunction,
    ))(input)
}


/// Matches an import statement.
///
/// An import statement consists of the keyword 'import' followed by a raw
/// string (no interpolated segments), the keyword 'as' and a binding pattern.
fn import<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, TopLevel, E> {
    map(
        tuple((
            preceded(
                postpad(keyword("import")),
                fail(positioned_postpad(preceded(
                    char('\"'),
                    terminated(raw_string, char('\"'))
                )), SyntaxElement::ImportPath),
            ),
            preceded(
                fail(postpad(keyword("as")), SyntaxElement::As),
                fail(postpad(binding), SyntaxElement::Binding),
            )
        )),
        |(path, binding)| TopLevel::Import(path, binding),
    )(input)
}


/// Matches a file.
///
/// A file consists of an arbitrary number of top-level statements followed by a
/// single expression.
fn file<'a, E: CompleteError<'a>>(
    input: Span<'a>,
) -> IResult<Span<'a>, File, E> {
    map(
        tuple((
            many0(postpad(import)),
            preceded(
                multispace0,
                terminated(
                    fail(expression, SyntaxElement::Expression),
                    fail(all_consuming(multispace0), SyntaxElement::EndOfInput)
                ),
            ),
        )),
        |(statements, expression)| File { statements, expression: expression.inner() },
    )(input)
}


/// Parse the input and return a [`File`] object.
pub fn parse(input: &str) -> Result<File, Error> {
    let span = Span::new(input);
    file::<SyntaxError>(span).map_or_else(
        |err| match err {
            NomError::Incomplete(_) => Err(Error::default()),
            NomError::Error(e) | NomError::Failure(e) => Err(e.to_error()),
        },
        |(_, node)| {
            node.validate()?;
            Ok(node)
        }
    )
}
