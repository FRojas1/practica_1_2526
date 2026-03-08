#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='p2pkg',
            executable='pub_ej2',
            name='nodopub_ejercicio2',
            namespace='miGrupo',
            remappings=[('/topic_ejercicio2', '/miGrupo/topic_ejercicio2')],
        ),
        Node(
            package='p2pkg',
            executable='sub_ej2',
            name='nodosub_ejercicio2',
            namespace='miGrupo',
            remappings=[('/topic_ejercicio2', '/miGrupo/topic_ejercicio2')],
        )
    ])
