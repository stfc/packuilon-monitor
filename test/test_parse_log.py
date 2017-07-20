from hypothesis import given, example, assume
import hypothesis.strategies as st
import packuilon_monitor.parse_log as pm


# # def test_
# @example('')
# @given(text())

@given(st.integers(0), st.integers(0))
def test_parse_valid_status_line(t, e):
    line = ('rabbit2packer: Build finished at ' +
            str(t) +
            ' (epoch) with exit code ' +
            str(e))
    assert pm.parse_status_line(line) == (t, e)

@given(st.text(),
       st.integers(),
       st.text(),
       st.integers())
def test_no_parse_invalid_status_line(s1, t, s2, e):
    # probably unnecessary, but serves as an example
    assume(s1 != 'rabbit2packer: Build finished at ' and
           s2 != ' (epoch) with exit code')
    line = (s1 +
            str(t) +
            s2 +
            str(e))
    assert pm.parse_status_line(line) != (t, e)
