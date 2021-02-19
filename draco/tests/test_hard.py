from draco import is_satisfiable
from draco.asp_utils import Block
from draco.programs import hard, helpers


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,text).

    :- violoation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,text).

    :- violoation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,y).

    :- violoation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,x).
    property(encoding,m1,e2).
    attribute(channel,e2,y).
    attribute(channel,e3,text).

    :- violoation(_).
    """
    )


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute(mark_type,m1,text).
    property(encoding,m1,e1).
    attribute(channel,e1,text).

    :- violoation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute(mark_type,m1,bar).
    property(encoding,m1,e1).
    attribute(channel,e1,text).

    :- violoation(_).
    """
    )
