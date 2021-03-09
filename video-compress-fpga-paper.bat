@REM @REM Evaluation function
@REM @REM Design by Trong-An Bui (trongan93@gmail.com) 
@REM @REM Advisor: Prof. Pei-Jun Lee
@REM @REM ViP Lab
@REM @REM NCNU
@REM set frame_number=12
@REM set gop=12
@REM set qp_i=2
@REM set qp_p=5

@REM set test_video_name_without_ext=taipei_260_271


@REM echo %test_video_name%_gop_%gop%_qp_i_%qp_i%_qp_p_%qp_p%_package_ >> Paper_Log_File
@REM python verification_demo_20201219_2.py -noui --qp_i %qp_i% --qp_p %qp_p% --gop %gop% --file %test_video_name_without_ext%.yuv --fn 12 --out %test_video_name_without_ext%
@REM echo 'Done to encoding'
@REM pause


set frame_number=12
set gop=(12,6,1) 
set qp_i=(2,4,8,16,31)
set p = 0

set test1_video_name_without_ext=taipei_260_271

(for %%g in %gop% do (
    (for %%i in %qp_i% do (
        set /a "p=%%i+3"
        @REM call echo %%p%%
        call python verification_demo_20201219_2.py -noui --qp_i %%i --qp_p %%p%% --gop %%g --file %test1_video_name_without_ext%.yuv --fn 12 --out %test1_video_name_without_ext%
    ))
    
))
echo 'Done to encoding'
pause


