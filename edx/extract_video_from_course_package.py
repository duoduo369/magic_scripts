#!/usr/bin/env python
'''
Extract edx course package video url and video id match to txt.

Setup:

    pip install arrow==0.16.0
    pip install click==7.1.2
    pip install beautifulsoup4==4.9.1

Usage:

    python extract_video_from_course_package.py -i /tmp/course-v1-MITx-6.00.1x-1T2020.tar.gz -o /tmp/1.txt
'''
import arrow
import click
import logging
import os
import sys
from bs4 import BeautifulSoup


log = logging.getLogger()
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
log.addHandler(stdout_handler)


def get_course_info(course_xml_path):
    with open(course_xml_path) as f:
        soup = BeautifulSoup(f)
    course_node = soup.course
    info = {
        'course': course_node['course'],
        'org': course_node['org'],
    }
    return info


def get_video_info(video_xml_path):
    with open(video_xml_path) as f:
        soup = BeautifulSoup(f)
    video_id = soup.video['edx_video_id']
    url = None
    dom = soup.video.find('source')
    if dom:
        url = dom['src']
    if not url:
        dom = soup.video.find('encoded_video', profile='desktop_mp4')
        url = dom['url']
    info = {
        'video_id': video_id,
        'url': url,
        'video_xml_path': video_xml_path,
    }
    return info


def write_video_infos(course, org, video_infos, output_path):
    template = '{video_url}\t{org}+{course}/{video_id}.mp4\n'
    with open(output_path, 'w') as f:
        for each in video_infos:
            video_url = each['url']
            video_id = each['video_id']
            if not video_url:
                log.warning('no url find in video_id: %s, please check again, %s',
                    video_id, each['video_xml_path'])
                continue
            row = template.format(video_url=video_url, org=org, course=course, video_id=video_id)
            f.write(row)


@click.command()
@click.option('--input_course_package_path', '-i', required=True, help="input data path")
@click.option('--output_path', '-o', required=True, help="output text path")
@click.option('--unzip_file_path', '-u', required=False,
        help="unzip course package path, if not provider, use /tmp/{timestamp}")
def run(input_course_package_path, output_path, unzip_file_path):
    if not unzip_file_path:
        unzip_file_path = '/tmp/{}'.format(arrow.now().timestamp)
    cmd = 'mkdir -p {} && tar zxf {} -C {}'.format(
        unzip_file_path, input_course_package_path, unzip_file_path
    )
    log.info('unzip course package: {}'.format(cmd))
    os.system(cmd)
    package_base_path = os.path.join(unzip_file_path, 'course')
    course_xml_path = os.path.join(package_base_path, 'course.xml')
    course_info = get_course_info(course_xml_path)
    course_video_dir = os.path.join(package_base_path, 'video')
    video_infos = (get_video_info(os.path.join(course_video_dir, each)) for each in os.listdir(course_video_dir))
    write_video_infos(course_info['course'], course_info['org'], video_infos, output_path)


if __name__ == '__main__':
    run()
