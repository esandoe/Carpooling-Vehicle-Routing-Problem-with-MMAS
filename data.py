datasets = {
    # Shallow zigzag
    '1': [
        (0, 0),  # start-node
        ((20, 5), (40, -5)),
        ((60, 5), (80, -5)),
        ((100, 5), (120, -5)),
        ((140, 5), (160, -5)),
        ((180, 5), (200, -5)),
    ],

    # Parallel trips, "V-shape"
    '2': [
        (30, 200),  # start-node
        ((0, 200), (60, 200)),
        ((2, 180), (58, 180)),
        ((1, 160), (59, 160)),
        ((4, 140), (56, 140)),
        ((3, 120), (57, 120)),
        ((6, 100), (54, 100)),
        ((5, 80), (55, 80)),
        ((8, 60), (52, 60)),
        ((7, 40), (53, 40)),
        ((10, 20), (50, 20)),
        ((9, 0), (51, 0)),
    ],

    # Five straight horizontal lines
    '3': [
        (-50, 90),  # start-node
        ((90, 170), (190, 170)),
        ((50, 170), (150, 170)),
        ((10, 170), (110, 170)),
        ((90, 130), (190, 130)),
        ((50, 130), (150, 130)),
        ((10, 130), (110, 130)),
        ((90, 90), (190, 90)),
        ((50, 90), (150, 90)),
        ((10, 90), (110, 90)),
        ((90, 50), (190, 50)),
        ((50, 50), (150, 50)),
        ((10, 50), (110, 50)),
        ((90, 10), (190, 10)),
        ((50, 10), (150, 10)),
        ((10, 10), (110, 10)),
    ],

    # Twelve spokes
    '4': [
        (0, 0),  # start-node
        ((0.0, 50.0), (0.0, 100.0)),
        ((25.0, 43.3), (50.0, 86.6)),
        ((43.3, 25.0), (86.6, 50.0)),
        ((50.0, 0.0), (100.0, 0.0)),
        ((43.3, -25.0), (86.6, -50.0)),
        ((25.0, -43.3), (50.0, -86.6)),
        ((0.0, -50.0), (0.0, -100.0)),
        ((-25.0, -43.3), (-50.0, -86.6)),
        ((-43.3, -25.0), (-86.6, -50.0)),
        ((-50.0, -0.0), (-100.0, -0.0)),
        ((-43.3, 25.0), (-86.6, 50.0)),
        ((-25.0, 43.3), (-50.0, 86.6)),
    ],

    # Ludo
    '5': [
        (65, 65),  # start-node
        ((10, 10), (10, 20)),
        ((110, 10), (110, 20)),
        ((110, 110), (110, 120)),
        ((10, 110), (10, 120)),
        ((20, 10), (20, 20)),
        ((120, 10), (120, 20)),
        ((120, 110), (120, 120)),
        ((20, 110), (20, 120)),
    ],
}
