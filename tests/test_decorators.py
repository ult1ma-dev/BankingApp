from pathlib import Path

import pytest

from src.decorators import log


def test_log(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def func(a: int | float, b: int | float) -> int | float:
        return a + b

    result = func(1, 2)
    captured = capsys.readouterr().out
    assert result == 3
    assert "func ok" in captured
    assert "Result of func work: 3" in captured


def test_log_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def func(a: int | float, b: int | float) -> float | int:
        return a + b

    func(1, 2)
    content = log_file.read_text(encoding="utf-8")
    assert "func ok" in content
    assert "Result of func work: 3" in content


def test_log_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def func(a: int | float, b: int | float = 0) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        func(1, 0)

    captured = capsys.readouterr().out

    assert "func error: division by zero. Inputs: (1, 0), {}" in captured
