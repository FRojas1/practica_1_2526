#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    numero_arg = DeclareLaunchArgument(
        'numero', default_value='7',
        description='Valor del campo numero del mensaje'
    )

    return LaunchDescription([
        numero_arg,
        Node(
            package='p2pkg',
            executable='pub_ej2',
            name='nodopub_ejercicio2',
            parameters=[{'numero': LaunchConfiguration('numero')}],
        ),
        Node(
            package='p2pkg',
            executable='sub_ej2',
            name='nodosub_ejercicio2',
        )
    ])
