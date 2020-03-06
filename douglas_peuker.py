from math import sqrt, pow


def point_to_line_Distance(point_a, point_b, point_c):
    """
    计算点a到点b c所在直线的距离
    :param point_a:
    :param point_b:
    :param point_c:
    :return:
    """
    # 首先计算b c 所在直线的斜率和截距
    if point_b[0] == point_c[0]:
        return 9999999
    slope = (point_b[1] - point_c[1]) / (point_b[0] - point_c[0])
    intercept = point_b[1] - slope * point_b[0]

    # 计算点a到b c所在直线的距离
    distance = abs(slope * point_a[0] - point_a[1] + intercept) / sqrt(1 + pow(slope, 2))
    return distance


def douglas_peuker(point_list, threshold):
    """

    道格拉斯-普克抽稀算法
    :param point_list: like [[122.358638, 30.280378], [122.359314, 30.280649]]
    :param threshold: 0.003
    :return:
    """
    def diluting(point_list, threshold, qualify_list, disqualify_list):
        """
        抽稀
        :param threshold:
        :param disqualify_list:
        :param qualify_list:
        :param point_list:二维点列表
        :return:
        """
        if len(point_list) < 3:
            qualify_list.extend(point_list[::-1])
        else:
            # 找到与收尾两点连线距离最大的点
            max_distance_index, max_distance = 0, 0
            for index, point in enumerate(point_list):
                if index in [0, len(point_list) - 1]:
                    continue
                distance = point_to_line_Distance(point, point_list[0], point_list[-1])
                if distance > max_distance:
                    max_distance_index = index
                    max_distance = distance

            # 若最大距离小于阈值，则去掉所有中间点。 反之，则将曲线按最大距离点分割
            if max_distance < threshold:
                qualify_list.append(point_list[-1])
                qualify_list.append(point_list[0])
            else:
                # 将曲线按最大距离的点分割成两段
                sequence_a = point_list[:max_distance_index]
                sequence_b = point_list[max_distance_index:]

                for sequence in [sequence_a, sequence_b]:
                    if len(sequence) < 3 and sequence == sequence_b:
                        qualify_list.extend(sequence[::-1])
                    else:
                        disqualify_list.append(sequence)
        return qualify_list, disqualify_list

    def get_qualify_list(point_list, threshold):
        qualify_list = list()
        disqualify_list = list()

        qualify_list, disqualify_list = diluting(point_list, threshold, qualify_list, disqualify_list)
        while len(disqualify_list) > 0:
            qualify_list, disqualify_list = diluting(disqualify_list.pop(), threshold, qualify_list, disqualify_list)

        return qualify_list

    # 当返回值长度小于4时，减小 threshold的值
    if len(point_list) < 5:
        return point_list
    result = get_qualify_list(point_list, threshold)
    if len(result) < 4:
        while len(result) < 4:
            threshold = threshold * 0.9
            result = get_qualify_list(point_list, threshold)

    if len(result) > len(point_list):
        return point_list

    return result
