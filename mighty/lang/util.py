import math
from .token import Token, Tokens

Position = tuple[int, int]


def distance(p1: Position, p2: Position) -> float:
    """Calculates the Euclidean distance between two points."""
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


def cumulative_distances(positions: list[Position]) -> list[float]:
    """Calculates cumulative distances along the given list of positions."""
    dists = [0.0]
    for i in range(1, len(positions)):
        dists.append(dists[-1] + distance(positions[i-1], positions[i]))
    return dists


def interpolate_position(p1: Position, p2: Position, t: float) -> Position:
    """Linearly interpolates between two positions based on factor t (0 <= t <= 1)."""
    x = p1[0] + t * (p2[0] - p1[0])
    y = p1[1] + t * (p2[1] - p1[1])
    return int(x), int(y)


def to_interval(positions: list[Position], old: int, new: int) -> list[Position]:
    """Adjusts a list of positions to match a new time interval."""
    if not positions or len(positions) < 2:
        return positions

    # Calculate the cumulative distances of the original positions.
    dists = cumulative_distances(positions)
    total_distance = dists[-1]

    # Determine the number of new points required based on the new interval
    num_points = int((total_distance / old) * new)

    # Generate new points spaced by the new interval
    new_positions = []
    new_interval_dist = total_distance / (num_points - 1) if num_points > 1 else total_distance

    current_dist = 0.0
    for i in range(1, len(positions)):
        # Interpolate between the current segment's points
        while current_dist <= dists[i]:
            # Calculate interpolation factor (0 <= t <= 1) within the current segment
            t = (current_dist - dists[i-1]) / (dists[i] - dists[i-1])
            new_positions.append(interpolate_position(positions[i-1], positions[i], t))
            current_dist += new_interval_dist

    # Ensure the final position is the exact end position
    if new_positions[-1] != positions[-1]:
        new_positions.append(positions[-1])

    return new_positions


def extract_position(segment: list[Token]) -> Position:
    """Extracts the position for a call."""
    if len(segment) != 6:
        raise SyntaxError("Invalid amount of tokens for function call.")

    return (int(segment[2][1]), int(segment[4][1]))


def reconstruct_tokens(positions: list[Position]) -> list[Token]:
    """Reconstructs tokens from interpolated Position tuples."""
    tokens = []
    for pos in positions:
        tokens.extend([
            (Tokens.IDENTIFIER, "mpos"),
            (Tokens.LPAREN, "("),
            (Tokens.NUMBER, str(pos[0])),
            (Tokens.COMMA, ","),
            (Tokens.NUMBER, str(pos[1])),
            (Tokens.RPAREN, ")")
        ])
    return tokens


def scale_tokens(tokens: list[Token], old_interval: int, new_interval: int) -> list[Token]:
    """Parses and injects interpolations in mpos sequences."""
    scaled: list[Token] = []  # Results of the scaling process.
    current_segment: list[Position] = []  # Positions for each consecutive call.
    current_call: list[Token] = []  # Tokens belonging to the current function call.
    inside_mpos = False
    last_mpos = False  # Used to close off segments.

    for token in tokens:
        if token[0] == Tokens.IDENTIFIER and token[1] == "mpos":
            # Start of an mpos sequence.
            inside_mpos = True
            current_call.append(token)
        elif inside_mpos and token[0] in [Tokens.NUMBER, Tokens.LPAREN, Tokens.COMMA, Tokens.RPAREN]:
            # Continue collecting tokens within the mpos call.
            current_call.append(token)
            last_mpos = True
            if token[0] == Tokens.RPAREN:
                # End of the mpos call; extract the position and reset for next.
                inside_mpos = False
                position = extract_position(current_call)
                current_segment.append(position)
                current_call = []
        elif last_mpos and token[0] == Tokens.EOL:
            # Complete the current segment after an EOL token.
            scaled_pos = to_interval(current_segment, old_interval, new_interval)
            reconstructed = reconstruct_tokens(scaled_pos)
            scaled.extend(reconstructed)  # Add the scaled tokens.
            last_mpos = False  # Reset last_mpos since the segment is done.
            current_segment = []
            scaled.append(token)  # Add the EOL or non-mpos token.
        else:
            # Append any non-mpos token that doesn't belong to a sequence.
            scaled.append(token)

    # Handle any remaining mpos segment (if it exists.)
    if current_segment:
        scaled_pos = to_interval(current_segment, old_interval, new_interval)
        reconstructed = reconstruct_tokens(scaled_pos)
        scaled.extend(reconstructed)

    return scaled
