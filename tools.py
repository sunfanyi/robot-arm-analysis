# -*- coding: utf-8 -*-
# @File    : tools.py
# @Time    : 06/02/2023
# @Author  : Fanyi Sun
# @Github  : https://github.com/sunfanyi
# @Software: PyCharm


from sympy import *
from IPython.display import display
# cos(theta)
# sin(theta)


def get_trans_mat(a, alpha, d, theta):
    """
    Obtain the transformation matrix from DH Parameters
    :param a: Link angle (in deg)
    :param alpha: Link twist
    :param d: Link offset (in deg)
    :param theta: Joint angle
    :return: transformation matrix and rotation matrix
    """
    if type(alpha) == int or type(alpha) == float:
        alpha = alpha*pi/180
    if type(theta) == int or type(theta) == float:
        theta = theta*pi/180

    R = rotation(alpha, 'x') * rotation(theta, 'z')
    T = add_translation(R, Matrix([a, 0, d, 1]))
    return R, T


def rotation(theta, direction):
    if direction == 'x':
        R = Matrix([[1, 0, 0],
                    [0, cos(theta), -sin(theta)],
                    [0, sin(theta), cos(theta)]])
    elif direction == 'y':
        R = Matrix([[cos(theta), 0, sin(theta)],
                    [0, 1, 0],
                    [-sin(theta), 0, cos(theta)]])
    elif direction == 'z':
        R = Matrix([[cos(theta), -sin(theta), 0],
                    [sin(theta), cos(theta), 0],
                    [0, 0, 1]])
    return R


def add_translation(R, t=Matrix([0, 0, 0, 1])):
    T = R.row_insert(len(R), Matrix([[0, 0, 0]]))
    T = T.col_insert(len(T), t)
    return T


def symprint(symbol, sup, sub, dot=False):
    if dot == 1:
        symbol = r'\dot{%s}' % symbol
    elif dot == 2:
        symbol = r'\ddot{%s}' % symbol
    info = r"^{}{}_{}".format(sup, symbol, sub)
    display(symbols(info))


def matprint(matrix, alias=None):
    if alias:
        display(matrix.subs(alias))
    else:
        display(matrix)


if __name__ == '__main__':
    t = symbols('t')
    theta = Function(r"\theta_1")(t)
    R = rotation(theta, 'z')
    matprint(R)
    symprint('R1G: ')
