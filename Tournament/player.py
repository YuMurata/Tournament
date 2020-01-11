from abc import ABCMeta, abstractclassmethod
import typing


class Player(metaclass=ABCMeta):
    '''
    implement decode(self)
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
    def decode(self):
        '''
        '''
        pass

    def score_up(self) -> typing.NoReturn:
        self.score *= 2

    def to_dict(self) -> dict:
        return {'score': self.score, 'param': self.param}


class PlayerGroup(metaclass=ABCMeta):
    '''implement
    
    score_up(self, index: int) -> NoReturn
    
    get_player(self, index: int) -> Player
    '''

    @abstractclassmethod
    def score_up(self, index: int) -> typing.NoReturn:
        pass

    @abstractclassmethod
    def get_player(self, index: int) -> Player:
        pass

TwoPlayer = typing.Tuple[Player, Player]