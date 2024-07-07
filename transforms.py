

def transform(self, x, y):
    #return self.transform_2D(x, y)
    return self.transform_perspective(x, y)


def transform_2D(self, x, y):
    return int(x), int(y)


def transform_perspective(self, x, y):
    line_y = y * self.perspective_point_y / self.height
    if line_y > self.perspective_point_y:
        line_y = self.perspective_point_y

    diff_x = x - self.perspective_point_x
    diff_y = self.perspective_point_y - line_y
    factor_y = pow(diff_y / self.perspective_point_y, 4)
    offset_x = diff_x * factor_y

    tr_x = self.perspective_point_x + offset_x
    tr_y = self.perspective_point_y * (1 - factor_y)
    return int(tr_x), int(tr_y)