import argparse
import numpy as np
import riffa
import time
import cv2
import processor as ps
import compare_pattern as cp
import bit_field

class ClassPatternCfg(object):
    def __init__(self,fileName,imgWidth,imgHeight,numReadFrame,waitForFPGA_sec):
        self.fileName = fileName
        self.imgWidth = imgWidth
        self.imgHeight = imgHeight
        self.numReadFrame = numReadFrame
        self.waitForFPGA_sec = waitForFPGA_sec
        self.imgSize = imgWidth * imgHeight
        self.cmpFile_bits = None
        self.cmpFile_MVs = None

# ----------------------------------------

class ClassVerificator(object):
    def __init__(self):
        self.header_and_info_byte = 8
        self.ME_blkWidth = 8
        self.ME_blkHeight = 8
        self.recvPackage = 0

        # # cmpFile_bits = cp.Class_cmpFile("","_","bin","Data/Source/result/",1,1)
        # # cmpFile_MVs = cp.Class_cmpFile("","_","bin","Data/Source/result/",1,1)
        # self.ptn_Burj_Khalifa_5 = ClassPatternCfg(
        #     "Burj_Khalifa_5.y"
        #     ,360
        #     ,240
        #     ,5
        #     ,2
        # )

        # ### -----------------------------------------

        # self.ptn_Artificial_imageries_2560_2560_12f_icons = ClassPatternCfg(
        #     "Artificial_imageries_2560_2560_12f_icons.yuv"
        #     ,2560
        #     ,2560
        #     ,12
        #     ,2
        # )
        # cmpFile_bits = cp.Class_cmpFile(
        #     "entropyBits"
        #     ,"_"
        #     ,"bin"
        #     ,"Data/Source/result/res_final_2560x2560/"
        #     ,0
        #     ,self.ptn_Artificial_imageries_2560_2560_12f_icons.numReadFrame
        # )
        # cmpFile_MVs = cp.Class_cmpFile(
        #     "MVs_bin"
        #     ,"_"
        #     ,"bin"
        #     ,"Data/Source/result/res_final_2560x2560/"
        #     ,1
        #     ,self.ptn_Artificial_imageries_2560_2560_12f_icons.numReadFrame-1
        # )
        # self.ptn_Artificial_imageries_2560_2560_12f_icons.cmpFile_bits = cmpFile_bits
        # self.ptn_Artificial_imageries_2560_2560_12f_icons.cmpFile_MVs = cmpFile_MVs

        # ### -----------------------------------------

        # self.ptn_all_black_2560x2560x12 = ClassPatternCfg(
        #     "all_black_2560x2560x12.y.y"
        #     ,2560
        #     ,2560
        #     ,12
        #     ,2
        # )
        # cmpFile_bits = cp.Class_cmpFile(
        #     "entropyBits"
        #     ,"_"
        #     ,"bin"
        #     ,"Data/Source/result/20200620_all_black_2560x2560x12_QP11_11/"
        #     ,0
        #     ,self.ptn_all_black_2560x2560x12.numReadFrame
        # )
        # cmpFile_MVs = cp.Class_cmpFile(
        #     "MVs_bin"
        #     ,"_"
        #     ,"bin"
        #     ,"Data/Source/result/20200620_all_black_2560x2560x12_QP11_11/"
        #     ,1
        #     ,self.ptn_all_black_2560x2560x12.numReadFrame-1
        # )
        # self.ptn_all_black_2560x2560x12.cmpFile_bits = cmpFile_bits
        # self.ptn_all_black_2560x2560x12.cmpFile_MVs = cmpFile_MVs

        self.QPP = 11
        self.QPI = 11
        self.GOP_case = 0
        self.GOP_num = 12
        self.fd = None

        self.SYS_DEFAULT_IMG_WIDTH = 2560
        self.SYS_DEFAULT_IMG_HEIGHT = 2560

        self.outFileName = ""

        self.procPattern = None

    def Flow_Verification(self):

        ####### Select test pattern #########

        procPattern = self.ptn_Artificial_imageries_2560_2560_12f_icons
        # procPattern2 = self.ptn_Artificial_imageries_2560_2560_12f_icons
        procPattern2 = self.ptn_all_black_2560x2560x12

        ####### Select test pattern #########


        


        print (riffa.fpga_list())
        self.fd = riffa.fpga_open(0)
        if (self.fd<0):	print ("Open fail")
        else:	
            for i in range(2):
                print ("Open success")


                if (i==0):
                    imgFrame = procPattern.numReadFrame
                    imgHeight = procPattern.imgHeight
                    imgWidth = procPattern.imgWidth
                    imgSize = procPattern.imgSize
                    waitForFPGA_sec = procPattern.waitForFPGA_sec
                    patternFileName = procPattern.fileName
                    self.imgFrame = procPattern.numReadFrame
                    self.imgHeight = procPattern.imgHeight
                    self.imgWidth = procPattern.imgWidth
                    self.imgSize = procPattern.imgSize
                    self.waitForFPGA_sec = procPattern.waitForFPGA_sec
                    self.patternFileName = procPattern.fileName
                    self.procPattern = procPattern
                else:
                    imgFrame = procPattern2.numReadFrame
                    imgHeight = procPattern2.imgHeight
                    imgWidth = procPattern2.imgWidth
                    imgSize = procPattern2.imgSize
                    waitForFPGA_sec = procPattern2.waitForFPGA_sec
                    patternFileName = procPattern2.fileName
                    self.imgFrame = procPattern2.numReadFrame
                    self.imgHeight = procPattern2.imgHeight
                    self.imgWidth = procPattern2.imgWidth
                    self.imgSize = procPattern2.imgSize
                    self.waitForFPGA_sec = procPattern2.waitForFPGA_sec
                    self.patternFileName = procPattern2.fileName
                    self.procPattern = procPattern2


                self.c2h_img = np.zeros([imgFrame,imgHeight,imgWidth],np.uint8)
                self.h2c_img = ps.OpenFileToVRaw(patternFileName,imgFrame,imgHeight,imgWidth)
                

                riffa.fpga_reset(self.fd)

                time.sleep(0.001)

                print ("Test pattern:%s"%(patternFileName))

                self.Flow_SendToDDR_Check()

                print (" ")
                print ("--------------------------------")
                print ("Wait H.264-like run")
                print ("--------------------------------")
                print (" ")
                time.sleep(waitForFPGA_sec)
                
                time.sleep(1)

                print (" ")
                print ("--------------------------------")
                print ("Recv H264 packet...")
                print ("--------------------------------")
                print (" ")
                self.RecvPacketFromPCIe()


            print("finish")
    
    def CmdFormatter_cfg(self):
        h2c_cmd = bit_field.ClassFormatter()

        CMD_ID = 1
        QPP = bit_field.ClassBitFieldUnit(5,self.QPP)
        QPI = bit_field.ClassBitFieldUnit(5,self.QPI)
        GOP_case = bit_field.ClassBitFieldUnit(3,self.GOP_case)
        resd = bit_field.ClassBitFieldUnit(15,0)
        cmd_id = bit_field.ClassBitFieldUnit(4,CMD_ID)

        h2c_cmd.fields.append (QPP)
        h2c_cmd.fields.append (QPI)
        h2c_cmd.fields.append (GOP_case)
        h2c_cmd.fields.append (resd)
        h2c_cmd.fields.append (cmd_id)

        h2c_cmd_raw = h2c_cmd.ConvertToBitUnit().GetValue()        
        h2c_cmd_np = np.array([h2c_cmd_raw],np.uint32)
        return (h2c_cmd_np)
    
    
    def CmdFormatter_dma(self,dmaOpIsh2c):
        h2c_cmd = bit_field.ClassFormatter()

        CMD_ID = 2 if (dmaOpIsh2c) else 3
        resd = bit_field.ClassBitFieldUnit(28,0)
        cmd_id = bit_field.ClassBitFieldUnit(4,CMD_ID)

        h2c_cmd.fields.append (resd)
        h2c_cmd.fields.append (cmd_id)

        h2c_cmd_raw = h2c_cmd.ConvertToBitUnit().GetValue()        
        h2c_cmd_np = np.array([h2c_cmd_raw],np.uint32)
        return (h2c_cmd_np)
    
    def CmdFormatter_start_H264(self):
        h2c_cmd = bit_field.ClassFormatter()

        CMD_ID = 4 
        resd = bit_field.ClassBitFieldUnit(28,0)
        cmd_id = bit_field.ClassBitFieldUnit(4,CMD_ID)

        h2c_cmd.fields.append (resd)
        h2c_cmd.fields.append (cmd_id)

        h2c_cmd_raw = h2c_cmd.ConvertToBitUnit().GetValue()        
        h2c_cmd_np = np.array([h2c_cmd_raw],np.uint32)
        return (h2c_cmd_np)
    


    def Flow_DEMO_1(self):
        print (riffa.fpga_list())
        self.fd = riffa.fpga_open(0)
        if (self.fd<0):	print ("Open fail")
        else:
            riffa.fpga_reset(self.fd)

            self.ConfigVerificator(11,11,0)

            # Cfg
            self.Flow_Cmd_Cfg()

            # PC -> DDR
            self.procPattern = self.ptn_Artificial_imageries_2560_2560_12f_icons
            self.Flow_Cmd_h2cImage()

            self.c2hRecvImg_Size = self.procPattern.imgSize
            self.c2hRecvImg_Width = self.procPattern.imgWidth
            self.c2hRecvImg_Height = self.procPattern.imgHeight
            self.Flow_Cmd_c2hImage()

            if (self.Compare_Pattern(self.h2c_img,self.c2h_img)):
                self.Flow_Cmd_startH264()

    def Compare_Pattern(self,ptn1_np,ptn2_np):
        print("compare pattern (DDR vs PC) ...",end="")
        if (np.array_equal(ptn1_np,ptn2_np)==False):
            print("mismath!")
            return (False)
        else:
            print("pass!")
            return (True)


    def ConfigVerificator(self,QPP,QPI,GOP_case):
        self.QPP = QPP
        self.QPI = QPI
        self.GOP_case = GOP_case
        LUT_GOP_num = [
            12
            ,6
            ,3
            ,2
            ,1
        ]
        try:
            self.GOP_num = LUT_GOP_num[self.GOP_case]
        except:
            self.GOP_num = LUT_GOP_num[len(LUT_GOP_num)-1]
    
    def Flow_Cmd_Cfg(self):
        # Cfg
        print("\n[Flow] config")
        h2c_cmd_np = self.CmdFormatter_cfg()
        riffa.fpga_send(self.fd,1,h2c_cmd_np,1,0,1,1000)

    def WritePattern(self):
        for i in range(self.testRound):
            fileNameStr = "QPI_%d__QPP_%d__GOP_%d__testPattern_%d.y"%(self.QPI,self.QPP,self.GOP_num,i)
            ps.OutputRaw_Y8(self.testPattern_lt[i],fileNameStr)

    def ReadTestPatternScript(self,ptnFileName):
        openVideoRaw = ps.OpenFileToVRaw (
            ptnFileName
            ,self.testFrameNum
            ,self.SYS_DEFAULT_IMG_HEIGHT
            ,self.SYS_DEFAULT_IMG_WIDTH
        )
        self.testRound = 1
        self.testPattern_lt = []
        self.testPattern_lt.append (openVideoRaw[0:self.GOP_num])


    def ReadTestPattern(self):
        ptnFileName = input("Pattern file name:")

        ptnFrame = int(input("Read file frames:"))
        
        openVideoRaw = ps.OpenFileToVRaw (
            ptnFileName
            ,ptnFrame
            ,self.SYS_DEFAULT_IMG_HEIGHT
            ,self.SYS_DEFAULT_IMG_WIDTH
        )

        print("\n")
        self.testRound = int(input("Test round:"))

        if (self.testRound<=1):
            self.testRound = 1
        
        self.testPattern_lt = []
        frameStart_lt = []
        frameEnd_lt = []
        for i in range(self.testRound):
            print("\n--- Set round %d ---"%(i))
            frameStart = int(input("Start frame num:"))
            frameEnd = int(input("End frame num:"))
            frameStart_lt.append (frameStart)
            frameEnd_lt.append (frameEnd)

            if (frameEnd > len(openVideoRaw)):
                print ("Start/end frame over than raw file! Reading failed!")
            self.testPattern_lt.append (openVideoRaw[frameStart:frameEnd+1])

        print ("\n\n--- info ----")
        for i in range(self.testRound):
            print ("Round[%d] frame %d -> %d"%(i,frameStart_lt[i],frameEnd_lt[i]))
        input("Press any key to continue... ")

    def Flow_Cmd_h2cImage(self):
        print("\n[Flow] h2c image")
        try:
            if (self.procPattern==None):
                return 0
        except:
            pass

        if (len(self.procPattern) < self.GOP_num):
            print("Abort operation: pattern frame less than GOP frame!")
        else :
            h2c_cmd_np = self.CmdFormatter_dma(1)
            riffa.fpga_send(self.fd,1,h2c_cmd_np,1,0,1,1000)

            self.h2c_img = self.procPattern
            for i in range(self.GOP_num):
                print ("Send h2c image[%d] ... "%(i),end="")
                # print (self.h2c_img[i][0][:20])
                sent = riffa.fpga_send(
                    self.fd
                    ,0
                    ,self.h2c_img[i]
                    ,self.h2c_img[i].shape[0]*self.h2c_img[i].shape[1]//4
                    ,0
                    ,True
                    ,5000)
                print ("sent:",sent)

    def Flow_Cmd_c2hImage(self):
        print("\n[Flow] c2h image")
        h2c_cmd_np = self.CmdFormatter_dma(0)
        riffa.fpga_send(self.fd,1,h2c_cmd_np,1,0,1,1000)
        self.c2h_img = np.zeros([self.GOP_num,self.c2hRecvImg_Height,self.c2hRecvImg_Width],np.uint8)
        for i in range(self.GOP_num):
            print ("Recv c2h image[%d] ... "%(i),end="")
            recv = riffa.fpga_recv(
                self.fd
                ,0
                ,self.c2h_img[i]
                ,5000
            )
            print ("recv:",recv)
    
    def Flow_Cmd_startH264(self,testRound):
        print("\n[Flow] start H264")
        h2c_cmd_np = self.CmdFormatter_start_H264()
        riffa.fpga_send(self.fd,1,h2c_cmd_np,1,0,1,1000)

        print("Wait FPGA encoding ...")
        time.sleep(1)

        print("Recv package ... ",end="")
        self.encodingPackage_bin = np.zeros([100*1024*1024],np.uint8)
        recv_rt_word = riffa.fpga_recv(self.fd,1,self.encodingPackage_bin,3000)
        recv_rt_byte = recv_rt_word<<2
        print ("byte:", recv_rt_byte , "(%.3f MB)"%(recv_rt_byte/1000/1000))
        
        try:
            if (self.outFileName==None):
                self.outFileName = "out"
        except:
            pass
        fileNameStr = "%s__QPI_%d__QPP_%d__GOP_%d__package_%d.bin"%(self.outFileName,self.QPI,self.QPP,self.GOP_num,testRound)
        ps.OutputRaw_Y8(self.encodingPackage_bin[:recv_rt_byte],fileNameStr)



    def Flow_Compare_FPGA_Python(self):
        
        num_bits = self.procPattern.numReadFrame
        num_mvs = num_bits-1
        cmpFile_FPGA_bit = cp.Class_cmpFile ("bitstream","_","bin","Data/Output/",0,num_bits)
        cmpFile_FPGA_mv = cp.Class_cmpFile ("motion_vector","_","bin","Data/Output/",0,num_mvs)


        cp.flow_compare(cmpFile_FPGA_bit,self.procPattern.cmpFile_bits,num_bits)
        print ("-----")
        cp.flow_compare(cmpFile_FPGA_mv,self.procPattern.cmpFile_MVs,num_mvs)

    def Flow_Debug_Recv(self):
        # Recv ref frame out from DDR
        for i in range(self.imgFrame-1):
            print("Recv c2h image")
            recvImgRefFrmOut = np.zeros([self.imgHeight*self.imgWidth],np.uint8)
            recv = riffa.fpga_recv(self.fd,0,recvImgRefFrmOut,3000)
            print ("[debug]recv out frame bytes:",recv<<2)

            fn = "out_frame_" + str(i) + ".bin"
            # ps.OutputRaw_Y8(self.c2h_img[i],fn)
            ps.OutputRaw_Y8(recvImgRefFrmOut,fn)


        # Recv bitstream
        self.recv_bits_lt = []
        self.bits_bytes_lt = []
        self.bits_total_len = 0
        for i in range(self.imgFrame):
            print("Recv c2h bitstream")
            recvBits = np.zeros([self.imgHeight*self.imgWidth*4],np.uint8)
            recv = riffa.fpga_recv(self.fd,0,recvBits,3000)
            bitstream_byte = recv<<2
            self.bits_bytes_lt.append ((bitstream_byte))
            bits_outFile = np.array(recvBits[:bitstream_byte],np.uint8)
            self.bits_total_len += (bitstream_byte)
            print ("bitstream bytes:",bitstream_byte)

            fn = "bitstream_" + str(i) + ".bin"
            ps.OutputRaw_Y8(bits_outFile,fn)

            self.recv_bits_lt.append (bits_outFile)
        
        # Recv MVs
        self.recv_mvs_lt = []
        for i in range(self.imgFrame-1):
            print("Recv c2h MVs")
            mvs_max = self.imgSize//self.ME_blkHeight//self.ME_blkWidth
            recv_max = pow(2,(mvs_max.bit_length()))
            recvMVs = np.zeros([recv_max],np.uint8)
            outMVs = np.zeros([mvs_max],np.uint8)
            recv = riffa.fpga_recv(self.fd,0,recvMVs,3000)
            outMVs[:] = recvMVs[:mvs_max]
            print ("recv motion vector bytes:",recv<<2)

            fn = "motion_vector_" + str(i) + ".bin"
            ps.OutputRaw_Y8(outMVs,fn)

            self.recv_mvs_lt.append (outMVs)
    
    def Flow_SendToDDR_Check(self):
        for i in range (self.imgFrame):
            print ("Send h2c image")
            print (self.h2c_img[i][0][:20])
            sent = riffa.fpga_send(self.fd, 0,self.h2c_img[i], self.imgSize//4, 0, True, 5000)
            print ("Sent:",sent)
        
        print ("Check pattern from DDR")

        for i in range (self.imgFrame):
            print ("Recv c2h image")
            recv = riffa.fpga_recv(self.fd, 0,self.c2h_img[i], 5000)
            print (self.c2h_img[i][0][:20])
            print ("Recv:",recv)

    def GetBitsMVsFromPacket(self):
        mv_size = self.imgWidth * self.imgHeight // self.ME_blkWidth // self.ME_blkHeight
        # est_total_size = self.header_and_info_byte + self.bits_total_len + mv_size * (self.imgFrame-1)
        est_total_size = self.header_and_info_byte + self.imgWidth*self.imgHeight*4*self.imgFrame + mv_size * (self.imgFrame-1)
        
        if (est_total_size>(self.packet_data.shape[0])):
            print ("Packet size error , total:%d , recv:%d"%(est_total_size,(self.packet_data.shape[0])))
        else:
            mvs_data_lt = []
            bits_data_lt = []

            if (est_total_size != (self.packet_data.shape[0])):
                self.packet_data = self.packet_data[:est_total_size]
                print ("PCIe transfer cause data size big than total size!")
            
            print ("Packet byte:",len(self.packet_data))
            packet_remain = self.packet_data[self.header_and_info_byte:]
            for i in range(self.imgFrame):
                if (i==0):
                    bits_data_lt.append(packet_remain[:self.bits_bytes_lt[i]])
                    print ("size:" , packet_remain[:self.bits_bytes_lt[i]].shape[0], "bytes:" , self.bits_bytes_lt[i])
                    packet_remain = packet_remain[self.bits_bytes_lt[i]:]
                else:
                    mvs_data_lt.append (packet_remain[:mv_size])
                    packet_remain = packet_remain[mv_size:]
                    
                    bits_data_lt.append(packet_remain[:self.bits_bytes_lt[i]])
                    print ("size:" , packet_remain[:self.bits_bytes_lt[i]].shape[0] , "bytes:" , self.bits_bytes_lt[i])
                    packet_remain = packet_remain[self.bits_bytes_lt[i]:]

            # Remain size check
            if (packet_remain.shape[0]):
                print ("Remain size error:",packet_remain.shape[0])
        
        return (bits_data_lt,mvs_data_lt)

    def RecvPacketFromPCIe(self):
        print ("Recv: packet")
        recv_max = 100*1024*1024
        recvPacket = np.zeros([recv_max],np.uint8)
        recv = riffa.fpga_recv(self.fd,1,recvPacket,5000)
        self.packet_data = recvPacket[:(recv<<2)]
        ps.OutputRaw_Y8(self.packet_data,"packet_%d.bin"%(self.recvPackage))
        self.recvPackage += 1
        print ("Word:" ,recv) 
        return (self.packet_data)

    # def script_start(self):


    def UI_start(self):
        self.ConfigVerificator(self.QPP,self.QPI,self.GOP_case)
        
        print (riffa.fpga_list())
        self.fd = riffa.fpga_open(0)
        if (self.fd<0):	print ("Open fail")
        else:
            riffa.fpga_reset(self.fd)

            for i in range(self.testRound):
                print ("Test round:%d"%(i))

                self.Flow_Cmd_Cfg()
                
                self.procPattern = self.testPattern_lt[i]
                self.Flow_Cmd_h2cImage()

                self.c2hRecvImg_Width = self.procPattern.shape[2]
                self.c2hRecvImg_Height = self.procPattern.shape[1]
                self.c2hRecvImg_Size = self.c2hRecvImg_Width * self.c2hRecvImg_Height
                self.Flow_Cmd_c2hImage()

                if (self.Compare_Pattern(self.h2c_img,self.c2h_img)!=True):
                    print ("Compare pattern DDR<->PC error!!")
                    return (0)

                self.Flow_Cmd_startH264(i)
                fileNameStr = "%s__QPI_%d__QPP_%d__GOP_%d__package_%d.yuv"%(self.outFileName,self.QPI,self.QPP,self.GOP_num,i)
                ps.OutputRaw_Y8(self.procPattern,fileNameStr)

    def ShowTitle(self):
        print("\n\n\n\
**********************************************************************\n\
* Copyright(c) 2020 LiscoTech Inc. & NCNU VIP Lab All right reserved\n\
* \n\
* H264 compression DEMO PC verification tool user interface\n\
* \n\
* Version: 0.0.0\n\
* \n\
* Date: 2020 1215\n\
* \n\
* Engineer: Kermit Chen\n\
**********************************************************************\n\
        ")

    def NON_UI(self):
        
        pass

    def UI(self):
        self.ShowTitle()

        while (1):
            print("\
================ Menm ================ \n\n\
Configuration:\n\
QP_I:%d / QP_P:%d / GOP_case:%d\n\n\
Operation:\n\
[1] Read test pattern\n\
[2] Set QP_I\n\
[3] Set QP_P\n\
[4] Set GOP_case\n\
[5] Start H264 compression\n\
[9] Output the test pattern\n\
----------\n\
[Q/q] Quit\n\
            "%(self.QPI,self.QPP,self.GOP_case))
            op = input('> ')
            try:
                op = int(op)
            except:
                if (op.lower()=="q"):
                    print("Quit...")
                    break
                else:
                    op = 0

            if (op==1):
                self.ReadTestPattern()

            elif (op==3 or op==2):
                strQP = "P" if (op==3) else "I"
                print("Set QP_%s"%(strQP))
                inVal = input('> ')
                try:
                    inVal = int(inVal)
                except:
                    inVal = 0
                if (op==3):
                    self.QPP = inVal
                else:
                    self.QPI = inVal

            elif (op==4):
                print("Set GOP_case")
                inVal = input('> ')
                try:
                    inVal = int(inVal)
                except:
                    inVal = 0
                self.GOP_case = inVal
                
            elif (op==5):
                self.UI_start()
            elif (op==9):
                self.WritePattern()
            else:
                print("Unknow operation")
            


            print("\n\n\n\n\n")
# ----------------------------------------




def OutputListToRawY8(lt,preName="out_file",extName="bin"):
    for i,lt_item in enumerate(lt):
        fn = "%s_%d.%s"%(preName,i,extName)
        ps.OutputRaw_Y8(lt_item,fn)


parser = argparse.ArgumentParser(description='H.264-Like Verification tool')
# parser.add_argument('--rp', dest='raw_path', type=str, help='raw/uncompress video path')
parser.add_argument('--fn', dest='frame_num', type=int, help='frame number')
parser.add_argument('--file', dest='testFile', type=str, help='test pattern file')
parser.add_argument('--gop', dest='gop', type=int, help='GOP value')
parser.add_argument('--qp_i', dest='qp_i', type=int, help='QP value for I frame')
parser.add_argument('--qp_p', dest='qp_p',type=int, help='QP value for P frame')
parser.add_argument('--out', dest='out_name',type=str, help='Ouput file name')
# parser.add_argument('--op', dest='output_path', type=str, help='output path for encoded result')
parser.add_argument('-noui', dest='noui', help='disable UI mode',action='store_true' )


if __name__ == '__main__':
    args = parser.parse_args()

    verificator = ClassVerificator()
    # verificator.Flow_Verification()
    # verificator.Flow_DEMO_1()
    if (args.noui):
        print ("No UI mode")
        verificator.NON_UI()
        verificator.GOP_num = args.gop
        verificator.QPI = args.qp_i
        verificator.QPP = args.qp_p
        verificator.outFileName = args.out_name
        if (args.gop == 12):
            verificator.GOP_case = 0
        elif (args.gop == 6):
            verificator.GOP_case = 1
        elif (args.gop == 3):
            verificator.GOP_case = 2
        elif (args.gop == 2):
            verificator.GOP_case = 3
        elif (args.gop == 1):
            verificator.GOP_case = 4
        else:
            print("GOP number error")

        verificator.testFrameNum = args.frame_num
        
        # verificator.ConfigVerificator()
        verificator.ReadTestPatternScript(args.testFile)
        verificator.UI_start()
        

    else:
        verificator.UI()