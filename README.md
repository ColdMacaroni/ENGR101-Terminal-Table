# ENGR101-Terminal-Table
Grabs the lecture schedule table for the current week and saves it to a file for you to cat

## Example
```
Link: https://ecs.wgtn.ac.nz/Courses/ENGR101_2023T1/LectureSchedule
Last Updated: 2023-02-26
You're on Week 1. This week starts on 2023-02-27
╒════════════════════════════╤════════════════════════════════╤═════════════════════════════╤═════════════════════════════╤══════════════════════════╕
│                            │ Day/Date                       │ Topic                       │ Slides                      │ TODOs                    │
╞════════════════════════════╪════════════════════════════════╪═════════════════════════════╪═════════════════════════════╪══════════════════════════╡
│ Week 1                     │ This is a lecture week         │                             │                             │                          │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Lecture 1                  │ Monday27 Feb                   │ Introduction to ENGR101     │ Intro to ENGR 101  Intro to │                          │
│                            │                                │ Howard, Arthur              │ Programming                 │                          │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Lecture 2                  │ Wednesday1 March               │ Computer architecture.      │ Lecture slides  Reading     │ Quiz1                    │
│                            │                                │ Computer data.  Binary      │ material                    │                          │
│                            │                                │ numbers.                    │                             │                          │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Lecture 3                  │ Friday3 March                  │ C++ Hello world, variables, │ Lecture slides  Reading     │ Quiz2  Quiz1 Due 3 March │
│                            │                                │ arrays  Arthur              │ material  InstallC          │ Midnight                 │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Quiz2 Due 4 March Midnight │                                │                             │                             │                          │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Lab A                      │ Maths Diagnostic Exercise      │                             │                             │                          │
├────────────────────────────┼────────────────────────────────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────┤
│ Lab B                      │ Tutorial 1 Part 1: Engineering │                             │                             │                          │
│                            │ Ethics  Tutorial 1 Part 2:     │                             │                             │                          │
│                            │ Sound Science and Technology   │                             │                             │                          │
│                            │ Due 6 March                    │                             │                             │                          │
╘════════════════════════════╧════════════════════════════════╧═════════════════════════════╧═════════════════════════════╧══════════════════════════╛
```

## .env
You need a .env on the same folder with stuff like
```
LINK="https://ecs.wgtn.ac.nz/Courses/ENGR101_2023T1/LectureSchedule"
LAST_UPDATE_FN="last_update"
SCHEDULE_OUT_FN="schedule"
```
I recommend absolute paths tho

## Use
Just slap this onto a dialy cron & add a `cat schedule` to your .whateverrc and boom easy win
