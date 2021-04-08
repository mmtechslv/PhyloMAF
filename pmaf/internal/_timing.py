#!/usr/bin/env python3

import time


class TimeBlock():

    def __init__(self, PieceDesccription):
        """
        Args:
            PieceDesccription:
        """
        self.start = time.time()
        self.comment = PieceDesccription

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Args:
            exc_type:
            exc_val:
            exc_tb:
        """
        end = time.time()
        runtime = round(end - self.start,2)
        msg = 'Piece [ {comment} ] took [ {time} ] seconds'
        print(msg.format(comment=self.comment, time=runtime))
