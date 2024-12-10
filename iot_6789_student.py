import time
from player import player
from stone import stone

class iot_6789_student(player):
    def __init__(self, clr):
        super().__init__(clr)
        self.time_limit = 2.5
        self.max_depth = 10
        self.start_time = None
        self.transposition_table = {}
        self.three_three = False

    def __del__(self):
        pass

    def next(self, board, length):
        print(" **** White player : My Turns **** ")
        self.start_time = time.time()
        stn = stone(self._color, length)

        opponent = -1 if self._color == 1 else 1

        # 1. 막히지 않은 4개가 있다면 5개로 완성하여 승리
        win_positions = self.find_winning_move(board, length, self._color)
        if win_positions:
            bx, by = win_positions[0]
            stn.setX(bx)
            stn.setY(by)
            print(" === 흑돌이 이길 준비를 합니다. === ")
            self.ensure_minimum_time()
            return stn
        # 2. 본인의 열린 3 연장 (조건: 상대의 위협이 낮은 경우)
        open_four_positions = self.find_fours(board, length, self._color)
        if open_four_positions:
            strongest_threat = self.evaluate_opponent_threat(board, length, opponent)
            if strongest_threat < 3000:  # 상대의 가장 강한 위협이 열린 5보다 낮은 경우
                bx, by = self.select_best_position(open_four_positions, length)
                stn.setX(bx)
                stn.setY(by)
                print(" === 흑돌이 자신의 열린 3을 연장하여 4목을 만듭니다. === ")
                self.ensure_minimum_time()
                return stn


        # 5. 닫힌5 차단 시도
        closed_five_positions = self.find_closed_fives(board, length, opponent)
        if closed_five_positions:
            bx, by = self.select_best_position(closed_five_positions, length)
            stn.setX(bx)
            stn.setY(by)
            print(" === 백돌의 닫힌 4를 처단합니다. === ")
            self.ensure_minimum_time()
            return stn

        # 2. 연속된 4개 차단 시도
        four_positions = self.find_fours(board, length, opponent)
        if four_positions:
            bx, by = self.select_best_position(four_positions, length)
            stn.setX(bx)
            stn.setY(by)
            print(" === 백돌의 4개 완성을 처단합니다. === ")
            self.ensure_minimum_time()
            return stn

        # 2. 쌍삼 상태에서는 3목 연장이 최우선
        if self.three_three:
            print(" === 쌍삼 상태에서 3목을 연장합니다. === ")
            extension_positions = self.find_extensions(board, length, self._color)
            if extension_positions:
                bx, by = extension_positions[0]
                stn.setX(bx)
                stn.setY(by)
                self.ensure_minimum_time()
                return stn
            else:
                print(" === 3목 연장이 불가능하여 기본 탐색으로 전환합니다. === ")


        # 4. 닫힌4 차단 시도
        closed_four_positions = self.find_one_side_closed_fours(board, length, opponent)
        if closed_four_positions:
            bx, by = self.select_best_position(closed_four_positions, length)
            stn.setX(bx)
            stn.setY(by)
            print(" === 백돌의 닫힌 4 완성시도를 처단합니다. === ")
            self.ensure_minimum_time()
            return stn
        # 2. 쌍삼을 만들 수 있는 위치를 탐색하여 사용
        double_open_three_positions = self.find_valid_double_open_threes(board, length, self._color)
        if double_open_three_positions:
            bx, by = double_open_three_positions[0]
            stn.setX(bx)
            stn.setY(by)
            print(" === 흑돌이 쌍삼을 만드려 합니다. === ")
            self.ensure_minimum_time()
            self.three_three = True
            return stn
        # 3. 열린3 차단 시도
        open_three_positions = self.find_open_threes(board, length, opponent)
        if open_three_positions:
            bx, by = self.select_best_position(open_three_positions, length)
            stn.setX(bx)
            stn.setY(by)
            print(" === 백돌의 이어질 3 완성시도를 처단합니다. === ")
            self.ensure_minimum_time()
            return stn

        # 7. 기본 알파베타 탐색 수행
        print("흑돌 공격 방안 고민 중...")
        candidates = self.generate_candidate_moves(board, length)
        best_move, best_score = self.alpha_beta_root(board, length, self.max_depth, candidates)
        stn.setX(best_move[0])
        stn.setY(best_move[1])
        print(" === 흑돌이 선택한 최적의 위치 === ")
        self.ensure_minimum_time()
        return stn

        center = (length - 1) // 2
        candidates.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))

        best_move = candidates[0]
        best_score = float('-inf')

        for depth in range(1, self.max_depth + 1):
            current_time = time.time() - self.start_time
            if current_time > self.time_limit or (current_time > 3 and depth > 1):
                break
            current_best_move, current_best_score = self.alpha_beta_root(board, length, depth, candidates)
            if time.time() - self.start_time > self.time_limit:
                break
            if current_best_score > best_score:
                best_score = current_best_score
                best_move = current_best_move

        stn.setX(best_move[0])
        stn.setY(best_move[1])
        print(" === White player chooses by advanced iterative deepening alpha-beta === ")
        self.ensure_minimum_time()
        return stn
    def find_extensions(self, board, length, color):
        """
        이 모든 코드는 황예강이 작성하였음.
        """
        positions = []
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    for dx, dy in directions:
                        if self.makes_four(board, length, x, y, color):
                            positions.append((x, y))
                            break
                    board[x][y] = 0
        return positions
    def generate_candidate_moves(self, board, length):
        """
        Generate a list of candidate moves sorted by proximity to the center.
        """
        candidates = [(x, y) for x in range(length) for y in range(length) if board[x][y] == 0]
        center = (length - 1) // 2
        candidates.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
        return candidates
    def find_valid_double_open_threes(self, board, length, color):
        """
        Find positions that create two valid open threes simultaneously.
        """
        positions = []
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 가로, 세로, 대각선1, 대각선2

        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:  # 빈 자리 탐색
                    open_three_directions = []
                    board[x][y] = color  # 현재 위치에 돌을 놓고 가정

                    # 각 방향에 대해 열린 3목 확인
                    for dx, dy in directions:
                        if self.makes_open_three_in_direction(board, length, x, y, color, dx, dy):
                            open_three_directions.append((dx, dy))

                    # 두 개 이상의 독립된 방향에서 열린 3목이 발견되면 쌍삼 후보
                    if len(open_three_directions) >= 2:
                        positions.append((x, y))

                    board[x][y] = 0  # 원상 복구

        return positions

    def makes_open_three_in_direction(self, board, length, x, y, color, dx, dy):
        """
        Check if placing a stone at (x, y) creates an open three in a specific direction.
        """
        count = 1  # 현재 위치에 돌을 놓았으므로 1부터 시작
        left_open = False
        right_open = False

        # 오른쪽 방향 탐색
        nx, ny = x + dx, y + dy
        while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
            count += 1
            nx += dx
            ny += dy
        if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
            right_open = True

        # 왼쪽 방향 탐색
        nx, ny = x - dx, y - dy
        while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
            count += 1
            nx -= dx
            ny -= dy
        if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
            left_open = True

        # 열린 3목인지 확인
        return count == 3 and left_open and right_open

    def ensure_minimum_time(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

    def alpha_beta_root(self, board, length, depth, moves):
        """
        Root function for Alpha-Beta pruning with support for 쌍삼 creation.
        """
        best_score = float('-inf')
        best_move = moves[0]
        alpha = float('-inf')
        beta = float('inf')
        for (x, y) in moves:
            if time.time() - self.start_time > self.time_limit:
                break
            board[x][y] = self._color
            score = self.alpha_beta(board, length, depth - 1, False, alpha, beta)
            board[x][y] = 0
            if score > best_score:
                best_score = score
                best_move = (x, y)
            alpha = max(alpha, best_score)
        return best_move, best_score

    # 알파베타 탐색
    def alpha_beta(self, board, length, depth, maximizing_player, alpha, beta):
        """
        Alpha-Beta pruning with 쌍삼 creation evaluation.
        """
        if time.time() - self.start_time > self.time_limit:
            return self.evaluate_board(board, length)

        if depth == 0:
            return self.evaluate_board(board, length)

        moves = self.generate_candidate_moves(board, length)

        if maximizing_player:
            value = float('-inf')
            for (x, y) in moves:
                if time.time() - self.start_time > self.time_limit:
                    break
                board[x][y] = self._color
                value = max(value, self.alpha_beta(board, length, depth - 1, False, alpha, beta))
                board[x][y] = 0
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = float('inf')
            opponent = -1 if self._color == 1 else 1
            for (x, y) in moves:
                if time.time() - self.start_time > self.time_limit:
                    break
                board[x][y] = opponent
                value = min(value, self.alpha_beta(board, length, depth - 1, True, alpha, beta))
                board[x][y] = 0
                beta = min(beta, value)
                if beta <= alpha:
                    break

        return value

    def find_winning_move(self, board, length, color):
        positions = []
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    if self.makes_five(board, length, x, y, color):
                        positions.append((x, y))
                    board[x][y] = 0
        return positions

    def makes_five(self, board, length, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            nx, ny = x + dx, y + dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx += dx
                ny += dy
            nx, ny = x - dx, y - dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx -= dx
                ny -= dy
            if count >= 5:
                return True
        return False

    def find_fours(self, board, length, color):
        positions = []
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    if self.makes_four(board, length, x, y, color):
                        positions.append((x, y))
                    board[x][y] = 0
        return positions

    def makes_four(self, board, length, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            left_open = False
            right_open = False

            nx, ny = x + dx, y + dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx += dx
                ny += dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                right_open = True

            nx, ny = x - dx, y - dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx -= dx
                ny -= dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                left_open = True

            if count == 4 and (left_open or right_open):
                return True
        return False

    def select_best_position(self, positions, length):
        center = (length - 1) // 2
        positions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
        return positions[0]



    def find_open_threes(self, board, length, color):
        open_three_positions = []
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    if self.makes_open_three(board, length, x, y, color):
                        open_three_positions.append((x, y))
                    board[x][y] = 0
        return open_three_positions

    def makes_open_three(self, board, length, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            left_open = False
            right_open = False

            nx, ny = x + dx, y + dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx += dx
                ny += dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                right_open = True

            nx, ny = x - dx, y - dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx -= dx
                ny -= dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                left_open = True

            if count == 3 and left_open and right_open:
                return True
        return False

    def find_one_side_closed_fours(self, board, length, color):
        closed_four_positions = []
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    if self.makes_one_side_closed_four(board, length, x, y, color):
                        closed_four_positions.append((x, y))
                    board[x][y] = 0
        return closed_four_positions

    def makes_one_side_closed_four(self, board, length, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            left_open = False
            right_open = False

            nx, ny = x + dx, y + dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx += dx
                ny += dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                right_open = True

            nx, ny = x - dx, y - dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx -= dx
                ny -= dy
            if 0 <= nx < length and 0 <= ny < length and board[nx][ny] == 0:
                left_open = True

            # 한쪽 닫힌4: count=4이고 한쪽만 열려있는 경우
            if count == 4 and ((left_open and not right_open) or (right_open and not left_open)):
                return True
        return False

    def find_closed_fives(self, board, length, color):
        closed_five_positions = []
        for x in range(length):
            for y in range(length):
                if board[x][y] == 0:
                    board[x][y] = color
                    if self.makes_closed_five(board, length, x, y, color):
                        closed_five_positions.append((x, y))
                    board[x][y] = 0
        return closed_five_positions

    def makes_closed_five(self, board, length, x, y, color):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1

            nx, ny = x + dx, y + dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx += dx
                ny += dy

            nx, ny = x - dx, y - dy
            while 0 <= nx < length and 0 <= ny < length and board[nx][ny] == color:
                count += 1
                nx -= dx
                ny -= dy

            if count == 5:
                return True
        return False

    def evaluate_board(self, board, length):
        my_score = self.pattern_score(board, length, self._color)
        opponent = -1 if self._color == 1 else 1
        opp_score = self.pattern_score(board, length, opponent)

        # 추가 점수: 쌍삼 생성 가능성 평가
        double_open_three_score = len(self.find_valid_double_open_threes(board, length, self._color)) * 5000

        return my_score - opp_score + double_open_three_score

    def evaluate_opponent_threat(self, board, length, opponent):
        score = 0

        four_positions = self.find_fours(board, length, opponent)
        if four_positions:
            score = max(score, 5000)

        open_three_positions = self.find_open_threes(board, length, opponent)
        if open_three_positions:
            score = max(score, 3000)  # 열린 3 위협

        return score

    def pattern_score(self, board, length, color):
        center = (length - 1) // 2
        score = 0
        stone_count = sum(1 for x in range(length) for y in range(length) if board[x][y] != 0)

        def line_pattern_count(line):
            segments = self.extract_segments(line, color)
            patterns = 0
            for seg, left_open, right_open in segments:
                seg_len = len(seg)
                open_ends = (1 if left_open else 0) + (1 if right_open else 0)
                if seg_len >= 5:
                    patterns += 10000000
                elif seg_len == 4:
                    if open_ends == 2:
                        patterns += 200000
                    elif open_ends == 1:
                        patterns += 10000
                elif seg_len == 3:
                    if open_ends == 2:
                        patterns += 3000
                    elif open_ends == 1:
                        patterns += 1000
                elif seg_len == 2:
                    if open_ends == 2:
                        patterns += 300
                    elif open_ends == 1:
                        patterns += 100
                elif seg_len == 1:
                    patterns += 30
            return patterns

        for x in range(length):
            score += line_pattern_count(board[x])
        for y in range(length):
            col = [board[x][y] for x in range(length)]
            score += line_pattern_count(col)
        for d in range(-length + 1, length):
            diag = [board[x][x - d] for x in range(length) if 0 <= x - d < length]
            if diag:
                score += line_pattern_count(diag)
            diag2 = [board[x][d - x] for x in range(length) if 0 <= d - x < length]
            if diag2:
                score += line_pattern_count(diag2)

        if stone_count < 10:
            for x in range(length):
                for y in range(length):
                    if board[x][y] == color:
                        dist = abs(x - center) + abs(y - center)
                        bonus = max(0, 200 - dist * 40)
                        score += bonus

        return score

    def extract_segments(self, line, color):
        segments = []
        current_seg = []
        line_length = len(line)

        for i, val in enumerate(line):
            if val == color:
                current_seg.append(i)
            else:
                if current_seg:
                    left_open = (current_seg[0] > 0 and line[current_seg[0] - 1] == 0)
                    right_open = (current_seg[-1] < line_length - 1 and line[current_seg[-1] + 1] == 0)
                    segments.append((current_seg, left_open, right_open))
                    current_seg = []
        if current_seg:
            left_open = (current_seg[0] > 0 and line[current_seg[0] - 1] == 0)
            right_open = (current_seg[-1] < line_length - 1 and line[current_seg[-1] + 1] == 0)
            segments.append((current_seg, left_open, right_open))
        return segments


