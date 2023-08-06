"""The lbsolver module provides classes and methods to solve the NYT Letter Boxed game.
"""
import argparse
from collections import defaultdict
from collections.abc import Iterator, Sequence
import sys
from typing import List, Optional, Union


class Gameboard:
    """This is a class that represents a Gameboard for a solver. Takes a string \
        representing the board.

        :param board: A string or list of strings that represent the board.
        :type board: list or str
        :raise ValueError: If the board is invalid (incorrect length, non-alphabet characters or repeated characters)
    """

    def __init__(self, board: Union[str, List[str]]) -> None:
        """This is the initialzer method."""

        if len(board) != 12:
            raise ValueError(
                f"{board} is not valid. Board must only be 12 unique alphabetic characters"
            )
        if isinstance(board, str):
            if not board.isalpha() or len(set(board)) != 12:
                raise ValueError(
                    f"{board} is not valid. Board must be alphabetic"
                    " characters only and 12 unique characters"
                )
        else:
            try:
                if not "".join(board).isalpha():
                    raise ValueError(
                        f"{board} is not valid. Board must be alphabetic characters only"
                    )
            except Exception as exc:
                raise ValueError(
                    f"{board} is not valid. Board must be alphabetic characters only"
                ) from exc
        self._board = "".join(board)

    @property
    def side1(self):
        """Get board side 1"""
        return self._board[0:3]

    @property
    def side2(self):
        """Get board side 2"""
        return self._board[3:6]

    @property
    def side3(self):
        """Get board side 3"""
        return self._board[6:9]

    @property
    def side4(self):
        """Get board side 4"""
        return self._board[9:12]

    @property
    def board(self):
        """The board represented as a list of strings"""
        return list(self._board)

    def __repr__(self) -> str:
        return f"""Board: {self.board}
        Side 1: {self.side1}
        Side 2: {self.side2}
        Side 3: {self.side3}
        Side 4: {self.side4}"""

    def get_side_for_letter(self, letter: str) -> Optional[str]:
        """Get the side a letter is on.

        :param letter: A string of length 1 with a single letter.
        :type letter: str
        :return: A str representing the side or None in case where the character is not on a side.
        :rtype: str or None
        """
        sides = [self.side1, self.side2, self.side3, self.side4]

        for side in sides:
            if letter in side:
                return side
        return None

    @staticmethod
    def default_board():
        """A utility method creating a default board that is known to generate results

        :return: A gameboard composed of 'giyercpolahx'
        :rtype: :class:`lbsolver.lbsolver.Gameboard`
        """
        return Gameboard("g i y e r c p o l a h x".split())


class LBSolver:
    """This is the solver class. It requires a :class:`lbsolver.lbsolver.Gameboard`
    and a dictionary to generate a set of answers to the Letter Boxed game.

    :param gameboard: A gameboard representing the letters in the Letter Boxed game
    :type gameboard: :class: `lbsolver.lbsolver.Gameboard`
    :param dictionary: A backing dictionary to use to find potential answers
    :type dictionary: Sequence[str]
    :raise TypeError: If gameboard or dictionary is set to None

    """

    def __init__(self, gameboard: Gameboard, dictionary: Sequence[str]) -> None:
        """Constructor method"""

        if gameboard is None:
            raise TypeError("Gameboard was set to None.")

        if dictionary is None:
            raise TypeError("Dictionary was set to None.")

        self.__gameboard = gameboard
        self.__dictionary = dictionary
        self.__answers: List[tuple] = []

    @property
    def gameboard(self) -> Gameboard:
        """A gameboard instance"""
        return self.__gameboard

    @gameboard.setter
    def gameboard(self, new_board: Gameboard):
        if new_board:
            self.__gameboard = new_board
        else:
            raise TypeError("gameboard cannot be set to None")

    @property
    def dictionary(self) -> Sequence[str]:
        """The dictionary instance"""
        return self.__dictionary

    @dictionary.setter
    def dictionary(self, dictionary: Sequence[str]):
        "Setting the dictionary"
        if dictionary:
            self.__dictionary = dictionary
        else:
            raise TypeError("dictionary cannot be set to None")

    def get_unused_letters(self, my_word: str) -> set:
        """Given a word, identify characters on the gameboard not used.

        :param my_word: A word to evaluate against the gameboard.
        :type my_word: str
        :raise ValueError: If the word contains characters not on the gameboard.
        :return: A set of unused characters from the gameboard.
        :rtype: set
        """
        my_word = my_word.strip()

        my_word_set = set(my_word)
        g_letters = set(list(self.gameboard.board))

        if my_word_set.difference(g_letters):
            raise ValueError(
                f"Word: {my_word} contains letters not found in gameboard: "
                f"{self.gameboard.board}"
            )
        return g_letters.difference(my_word_set)

    def possible_on_board(self, word_sequence: str) -> bool:
        """Check whether a sequence is possible based upon Letter Boxed rules. It
        does not determine whether the sequence is a word.

        :param word_sequence: Check whether a potential word is possible on the board.
        :type word_sequence: str
        :return: True if sequence is possible on board, false otherwise
        :rtype: bool
        """
        valid_sequence = True
        first_let, second_let = ("", "")
        for first_let, second_let in zip(word_sequence, word_sequence[1:]):
            if first_let == second_let:
                valid_sequence = False
                break
            side = self.gameboard.get_side_for_letter(first_let)
            # side = get_side(a, [side1, side2, side3, side4])
            if not side:
                valid_sequence = False
                break
            elif second_let in side:
                valid_sequence = False
                break

        if not self.gameboard.get_side_for_letter(second_let):
            return False
        return valid_sequence

    def generate_valid_words(
        self, dictionary: Optional[Sequence[str]] = None
    ) -> Iterator[str]:
        """Based on the current gameboard, generate a set of valid words from
        dictionary. If dictionary parameter is not set, default dictionary is used.

        :param dictionary: An dictionary to use to find valid words
        :type dictionary: Sequence[str]
        :return: A set of valid words
        :rtype: Iterator[str]
        """
        if not dictionary:
            dictionary = self.dictionary

        for item in dictionary:
            item = item.strip()
            if not item:
                continue
            if (
                item[0].islower()
                and len(item) >= 3
                and all(letter in self.gameboard.board for letter in item.lower())  # type: ignore
            ):
                item = item.lower().strip()

                valid_word = self.possible_on_board(item)
                if valid_word:
                    yield item
            else:
                continue

    def solve(
        self, max_num_words: int = 3, minimum_answers: int = 1, skip: str = ""
    ) -> Sequence[tuple]:
        """Solve the puzzle based on the current dictionary and gameboard.

        :param max_num_words: The maximum number of words allowed in an answer
        :type max_num_words: int
        :param minimum_answers: The minimum number of answers to retrieve. Solve
        will stop after finding this number of answers
        :type minimum_answers: int
        :param skip: A list of words separated by commas. Words in this list will be skipped
        from answers
        :type skip: str
        :raise ValueError: if max_num_words or minimum_answers is less than or equal to zero.
        :return: A list filled with answer tuples
        :rtype: Sequence[tuple]
        """
        self.__answers.clear()

        if max_num_words <= 0:
            raise ValueError("max_num_words must be greater than zero")

        if minimum_answers <= 0:
            raise ValueError("minimum_answers must be greater than zero")

        word_ranking_map = defaultdict(list)
        valid_words = set(self.generate_valid_words())
        for word in valid_words:
            num_letters_used = len(self.gameboard.board) - len(
                self.get_unused_letters(word)
            )
            word_ranking_map[(num_letters_used, word[0])].append(word)
        sorted_keys = sorted(word_ranking_map, reverse=True)
        used = set()
        skip_list = list(skip_word.strip() for skip_word in skip.lower().split(","))

        def dfs(word: str, possible_answer: tuple):
            if any(
                word.lower().strip() == answer.lower().strip()
                for answer in possible_answer
            ):
                return

            if len(self.__answers) >= minimum_answers or word in skip_list:
                return

            if (
                len(possible_answer) >= max_num_words
                or word in used
                or word not in valid_words
            ):
                return
            possible_answer = possible_answer + (word,)
            letters_left = self.get_unused_letters("".join(possible_answer))
            if letters_left:

                filter_keys = (key for key in sorted_keys if key[1] == word[-1])
                for key in sorted(filter_keys, reverse=True):
                    for next_word in word_ranking_map[key]:
                        dfs(next_word, possible_answer)
            else:
                used.update(possible_answer)
                self.__answers.append(possible_answer)
                return

        for key in sorted_keys:
            if len(self.__answers) >= minimum_answers:
                break
            for word in word_ranking_map[key]:
                if word.lower() not in skip_list:
                    dfs(word, tuple())
        return self.__answers


def main():  # pragma: no cover
    """Main function"""
    parser = argparse.ArgumentParser(
        prog="lbsolver",
        description="Generate solutions to the NYT Letter-Boxed puzzle",
    )
    parser.add_argument(
        "board",
        help="A string representing the board in format 'abcdefghijkl' where each group of 3 letters represents a side. ",
        nargs="?",
        default="giyercpolahx",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--dictionary",
        metavar="dictionary",
        help="The path to a dictionary for the puzzle to select words from."
        "Should be a text file.",
        type=argparse.FileType("r"),
        default="/usr/share/dict/words",
    )

    parser.add_argument(
        "-a",
        "--answer-size",
        metavar="total_words",
        help="Maximum number of words allowed in an answer",
        type=int,
        default=3,
    )

    parser.add_argument(
        "-t",
        "--total-answers",
        metavar="answers",
        help="The number of answers you want back.",
        type=int,
        default=10,
    )

    parser.add_argument(
        "-s",
        "--skip",
        metavar="skipwords",
        help="A comma separated list of words to not use in the answer-set",
        type=str,
        default="",
    )

    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Output file for results. Defaults to standard out",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )

    args = parser.parse_args()

    try:
        myboard = Gameboard(args.board)
        dictionary_words = args.dictionary.readlines()
        solver = LBSolver(myboard, dictionary_words)
        final_answers = solver.solve(
            max_num_words=args.answer_size,
            minimum_answers=args.total_answers,
            skip=args.skip,
        )
    except ValueError as exc1:
        parser.print_usage(sys.stderr)
        if "Board must" in str(exc1):
            print(
                "LBSolver: error: board is not valid. It must be only 12 unique alphabetic characters.",
                file=sys.stderr,
            )
        else:
            print(
                f"LBSolver: error: {'answer_size' if 'minimum_answers' in str(exc1) else 'total_answers'}"
                " must be greater than zero.",
                file=sys.stderr,
            )
        args.output.close()
        sys.exit(1)

    if final_answers:
        for a_id, answer in enumerate(final_answers, start=1):
            print(f"Answer {a_id:>2}: {'---'.join(answer)}", file=args.output)
    else:
        print(
            "No answers for given board and dictionary for requested answer size",
            file=args.output,
        )
    args.output.close()


if __name__ == "__main__":
    main()
