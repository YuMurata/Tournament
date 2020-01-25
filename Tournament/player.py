from abc import ABCMeta, abstractclassmethod
import typing


class Player(metaclass=ABCMeta):
    '''
    implement
    ---
    decode(self)

    decode so that you can compare

    - - -
    player has __init__(self, param: typing.Any, score: int = 1)
    '''

    def __init__(self, param: typing.Any, score: int = 1):
        '''
        Parameters
        ----------
        param : Any
        score : int = 1
        '''

        self.param = param
        self.score = score

    @abstractclassmethod
    def decode(self) -> typing.Any:
        '''
        '''
        pass

    def score_up(self) -> typing.NoReturn:
        self.score *= 2

    def to_dict(self) -> dict:
        return {'score': self.score, 'param': self.param}


TwoPlayer = typing.Tuple[Player, Player]
PlayerList = typing.List[Player]
