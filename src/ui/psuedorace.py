BEGIN

    Create application

    Load track data

    Create race controller
    Configure race controller
    Create race window
    Display race window

    WHILE application is running

        IF race is not finished THEN

            Advance race simulation by one step

            FOR EACH car

                Calculate current progress around track
                Convert progress into screen position
                Store screen position

            END FOR

            Redraw race display

                Draw background
                Draw track
                Draw checkpoints

                FOR EACH car

                    Select display colour
                    Draw car at stored position
                    Draw driver label

                END FOR

        ELSE

            Stop race timer

            Sort cars by race progress

            Display final race results

        END IF

    END WHILE

END