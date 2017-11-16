#!/usr/bin/env python
import subprocess

COLUMN_DIVIDERS = ','.join(map(str, [
  55,80,95,130,150,210,295,360,420,480,550
]))

def parse_dir_pdf(pdf):
  subject = None
  term = None # term should be same for entire file

  process = subprocess.Popen([
    'java', 
    '-jar', 
    'tabula-1.0.1-jar-with-dependencies.jar', 
    pdf,
    '--columns=' + COLUMN_DIVIDERS,
    '--format=TSV',
    '--pages=all'
  ], stdout=subprocess.PIPE)

  out, err = process.communicate()

  sections = []

  for row in out.split("\r\n"):
    cols = row.split("\t")
    joined = ''.join(cols)

    if 'SUBJECT' in joined:
      dept_num = int(joined[-4:-1])

    if 'TERM:' in joined:
      term = int(joined.split(':')[-1])

    # valid rows have 12 columns
    if len(cols) != 12:
      continue

    # valid rows should have a course number
    # if it does not parse, we skip this row
    try:
      int(cols[1])
    except ValueError:
      continue
    
    # unknown values: cols[0], cols[4]

    course_num = int(cols[1])
    section_type = cols[2]
    section_num = cols[3]
    time = cols[5]
    days = cols[6]
    facility = cols[7]
    combined_enrollment = cols[8]
    total_enrollment = cols[9]
    instructor_id = cols[10]
    instructor_name = cols[11]

    # if combined enrollment is not defined, that means
    # it is not cross listed
    if combined_enrollment == '':
      combined_enrollment = None

    if time == '-':
      start_time = None
      end_time = None
    elif ' - ' in time:
      split_time = time.split(' - ')
      start_time = split_time[0]
      end_time = split_time[1]

    if len(days) == 0:
      days_array = []
    else:
      days_array = days.split(' ')

    if facility in ('ONLINE', 'OFF CAMPUS'):
      building = facility
      room = None
    elif facility == '':
      building = None
      room = None
    elif ' ' in facility:
      parts = facility.split(' ')
      building = parts[0]
      room = parts[1]
    elif len(facility) > 8:
      building = facility[0:5]
      room = facility[5:]
    else:
      print('Unable to parse facility: "%s"' % facility)
      building = None
      room = None

    sections.append({
      "dept_num": dept_num,
      "course_num": course_num,
      "section_num": section_num,
      "start_time": start_time,
      "end_time": end_time,
      "days": days_array,
      "building": building,
      "room": room,
      "combined_enrollment": combined_enrollment,
      "total_enrollment": total_enrollment,
      "instructor_id": instructor_id,
      "instructor_name": instructor_name
    })
  return sections