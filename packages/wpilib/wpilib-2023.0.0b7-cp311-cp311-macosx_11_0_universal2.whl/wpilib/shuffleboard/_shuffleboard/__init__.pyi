from __future__ import annotations
import wpilib.shuffleboard._shuffleboard
import typing

__all__ = [
    "BuiltInLayouts"
]


class BuiltInLayouts():
    """
    The types of layouts bundled with Shuffleboard.

    <pre>{@code
    ShuffleboardLayout myList = Shuffleboard::GetTab("My Tab")
    .GetLayout(BuiltinLayouts::kList, "My List");
    }</pre>

    Members:

      kList : Groups components in a vertical list. New widgets added to the layout will
    be placed at the bottom of the list. 
    Custom properties: <table>
    <tr><th>Name</th><th>Type</th><th>Default Value</th><th>Notes</th></tr>
    <tr><td>Label position</td><td>String</td><td>"BOTTOM"</td>
    <td>The position of component labels inside the grid. One of
    ``["TOP", "LEFT", "BOTTOM", "RIGHT", "HIDDEN"``</td></tr>
    </table>

      kGrid : Groups components in an *n* x *m* grid. Grid layouts default to
    3x3. 
    Custom properties: <table>
    <tr><th>Name</th><th>Type</th><th>Default Value</th><th>Notes</th></tr>
    <tr><td>Number of columns</td><td>Number</td><td>3</td><td>Must be in the
    range [1,15]</td>
    </tr>
    <tr><td>Number of rows</td><td>Number</td><td>3</td><td>Must be in the
    range [1,15]</td></tr> <tr> <td>Label position</td> <td>String</td>
    <td>"BOTTOM"</td>
    <td>The position of component labels inside the grid.
    One of ``["TOP", "LEFT", "BOTTOM", "RIGHT", "HIDDEN"``</td>
    </tr>
    </table>
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'kList': <BuiltInLayouts.kList: 0>, 'kGrid': <BuiltInLayouts.kGrid: 1>}
    kGrid: wpilib.shuffleboard._shuffleboard.BuiltInLayouts # value = <BuiltInLayouts.kGrid: 1>
    kList: wpilib.shuffleboard._shuffleboard.BuiltInLayouts # value = <BuiltInLayouts.kList: 0>
    pass
