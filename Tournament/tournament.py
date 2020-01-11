from enum import Enum, auto
from random import sample
import logging
from .type_hint import PlayerList, TwoPlayer
import typing
from .player import PlayerGroup


class TournamentException(Exception):
    pass


class RoundException(TournamentException):
    pass


class MatchException(TournamentException):
    pass


class CompeteException(TournamentException):
    pass


class CompleteException(TournamentException):
    pass


class GameWin(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTH_WIN = auto()
    BOTH_LOSE = auto()


class Tournament:
    @classmethod
    def make_player_index_list(cls, player_num: int) -> (list, list):
        current_player_index_list = list(range(player_num))
        current_player_index_list = \
            sample(current_player_index_list, player_num)

        next_player_index_list = []

        return current_player_index_list, next_player_index_list

    def __init__(self, player_group: PlayerGroup,
                 current_player_index_list: list, next_player_index_list: list,
                 *, handler: logging.StreamHandler = None):
        self.logger = logging.getLogger('Tournament')
        self.logger.setLevel(logging.INFO)

        if handler is not None:
            self.logger.addHandler(handler)

        self.player_group = player_group

        self.current_player_index_list = current_player_index_list

        self.next_player_index_list = next_player_index_list

        self.old_player_num = \
            len(current_player_index_list)+len(next_player_index_list)

        self.is_match = False
        self.is_complete = False

        self.round_count = 1
        self.match_count = 0

        self.logger.debug('init')

        self.logger.info(f'--- game start ---')
        self._log_start_round()

    def _log_start_round(self):
        self.logger.info(f'start {self.round_count}th round')
        self.logger.info(
            f'--- current player index: {self.current_player_index_list} ---')
        score_list = [player.score for player in self.player_list]
        self.logger.info(f'--- score: {score_list} ---')

    def _new_round(self):
        if len(self.current_player_index_list) >= 2:
            raise RoundException('invalid round')

        for index in self.current_player_index_list:
            self.player_group.score_up(index)

        self.next_player_index_list.extend(self.current_player_index_list)
        self.current_player_index_list = \
            sample(self.next_player_index_list,
                   len(self.next_player_index_list))
        self.next_player_index_list.clear()

        current_player_num = len(self.current_player_index_list)
        is_no_change_player_num = current_player_num == self.old_player_num
        is_no_player = current_player_num < 2
        self.is_complete = is_no_change_player_num or is_no_player

        self.old_player_num = len(self.current_player_index_list)

        self.round_count += 1
        self.match_count = 0

        self._log_start_round()

    def new_match(self) -> (bool, TwoPlayer):
        if self.is_match:
            raise MatchException('match is already ready')

        if self.is_complete:
            raise CompleteException('game is already over')

        self.logger.info(f'--- new match start ---')

        if len(self.current_player_index_list) >= 2:
            self.left_player_index = self.current_player_index_list.pop()
            self.right_player_index = self.current_player_index_list.pop()
            self.is_match = True

            self.match_count += 1

            left_player = \
                self.player_group.get_player(self.left_player_index)
            right_player = \
                self.player_group.get_player(self.right_player_index)

            self.logger.info(
                f'--- left player index: {self.left_player_index} ---')
            self.logger.info(
                f'--- right player index: {self.right_player_index} ---')

            return (False, (left_player, right_player))

        else:
            self._new_round()
            if self.is_complete:
                return (True, None)
            else:
                return self.new_match()

    def compete(self, winner: GameWin) -> typing.NoReturn:
        if not self.is_match:
            raise CompeteException('match is not ready yet')

        if self.is_complete:
            raise CompleteException('game is already over')

        def _win(winner_index: int):
            self.player_list[winner_index].score_up()
            self.next_player_index_list.append(winner_index)

        if winner == GameWin.BOTH_WIN:
            _win(self.left_player_index)
            _win(self.right_player_index)
        elif winner == GameWin.LEFT:
            _win(self.left_player_index)
        elif winner == GameWin.RIGHT:
            _win(self.right_player_index)

        self.logger.info(f'--- winner: {winner.name} ---')
        self.is_match = False

        is_no_current_player = len(self.current_player_index_list) == 0
        is_only_one_winner = len(self.next_player_index_list) == 1
        is_championship = is_no_current_player and is_only_one_winner
        is_no_player = is_no_current_player and len(
            self.next_player_index_list) == 0

        if is_championship or is_no_player:
            self.is_complete = True

    @property
    def get_match_num(self):
        current_match_num = len(self.current_player_index_list)-1
        next_match_num = len(self.next_player_index_list)
        return current_match_num+next_match_num
