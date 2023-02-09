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


def plot_links(ax, links, show_coor=False):
    for i in range(len(links)-1):
        P1 = links[i][:3]
        P2 = links[i+1][:3]
        ax.plot([P1[0], P2[0]], [P1[1], P2[1]], [P1[2], P2[2]], 'b-')
        ax.plot([P1[0]], [P1[1]], [P1[2]], 'bx')

        if show_coor:
            P1 = [round(i) for i in P1]
            P2 = [round(i) for i in P2]
            if P1 != P2:
                ax.text(P1[0] - 10, P1[1], P1[2] + 3, str(P1))
    if show_coor:
        ax.text(P2[0] - 10, P2[1], P2[2] - 15, str(P2))


def plot_links_moving(line1, line2, links):
    link_data = [[], [], []]
    joint_data = [[], [], []]
    for i in range(len(links)-1):
        P1 = links[i][:3]
        P2 = links[i+1][:3]

        # Link line
        link_data[0].extend([P1[0], P2[0]])
        link_data[1].extend([P1[1], P2[1]])
        link_data[2].extend([P1[2], P2[2]])

        # Joint point
        joint_data[0].extend([P1[0]])
        joint_data[1].extend([P1[1]])
        joint_data[2].extend([P1[2]])

    line1.set_xdata(link_data[0])
    line1.set_ydata(link_data[1])
    line1.set_3d_properties(link_data[2])

    # Joint point
    line2.set_xdata(joint_data[0])
    line2.set_ydata(joint_data[1])
    line2.set_3d_properties(joint_data[2])


def joint_print(joints, alias):
    for i in range(len(joints)):
        print('Joint %d position:' % (i+1))
        matprint(joints[i], alias)


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
    R.simplify()
    T = add_translation(R, Matrix([a, -sin(alpha) * d, cos(alpha) * d, 1]))
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
