import subprocess

process = subprocess.Popen([
  'java', 
  '-jar', 
  'tabula-1.0.1-jar-with-dependencies.jar', 
  '1182-Final-DIR-Report.pdf',
  '--columns=55,80,95,130,150,210,295,360,420,480,550',
  '--format=TSV',
  '--pages=all'
], stdout=subprocess.PIPE)

out, err = process.communicate()

for row in out.split("\r\n"):
  cols = row.split("\t")

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

  course_number = int(cols[1])
  section_type = cols[2]
  section_number = cols[3]
  time = cols[5]
  days = cols[6]
  facility = cols[7]
  combined_enrollment = cols[8] # combines cross-listed courses
  total_enrollment = cols[9]
  instructor_id = cols[10]
  instructor = cols[11]
