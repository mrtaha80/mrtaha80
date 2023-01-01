

def fp():

    lc=0

    for code in test:

        flag=0

        for i  in memo_Ref_list+reg_Ref_list+io_Ref_list+pscode_list:
            if i == code[0:3]:
                flag=1

        if flag==0:
            symbol_table.append([code[0:3],lc])
            lc +=1
            
        else:
            if code[0:3]=="ORG":
                lc=int(code[4:])
                
            else:
                if code[0:3]=="END":
                    sp()
                    return
                else:
                    lc +=1

def sp():
    lc=0
    for code in test:
        instStr = 0
        if len(code) > 3:
            if code[3] == ',':
                instStr = 5
        flag=0
        for i in pscode_list:
            if code[instStr:instStr+3] == i:
                flag=1
        if flag ==1:
            if code[0:3] == "ORG":
                lc = int(code[4:])
                
            else:
                if code[0:3] == "END":
                    print('your done')
                    return
                else:
                    if code[instStr:instStr+3] == "DEC":
                        key = twoscomplement(int(code[4+instStr:]))

                    elif code[instStr:instStr+3] == "HEX":
                        key = twoscomplement(int(code[4+instStr:], 16))
                    
                    first=0
                    if key[0]=="1":
                        first=1

                    collector = []
                    for i in range(16):
                        collector += str(first)

                    for i in range(len(key)-first):
                        collector[-i-1] = key[-i-1]

                    give = ''
                    for i in range(len(collector)):
                        give += collector[i]
                    give_file.write(str(bin(lc))[2:] + '\t'+give+'\n')
                    lc += 1                    
        else:

            mri_flag = 0
            for i in memo_Ref_list:
                if code[instStr:instStr+3] == i:
                    mri_flag = 1

            if mri_flag:
                give = ''

                if code[-2] == 'i' or code[-2] == 'I':
                    give += '1'
                else:
                    give += '0'

                if code[instStr:instStr+3] =='AND':
                    give += '000'
                elif code[instStr:instStr+3] =='ADD':
                    give += '001'
                elif code[instStr:instStr+3] =='LDA':
                    give += '010'
                elif code[instStr:instStr+3] =='STA':
                    give += '011'
                elif code[instStr:instStr+3] =='BUN':
                    give += '100'
                elif code[instStr:instStr+3] =='BSA':
                    give +='101'
                else:
                    give +='110'

                for i in symbol_table:
                    if code[instStr+4:instStr+7] == i[0]:
                        temp = ['0', '0', '0', '0', '0', '0',
                                '0', '0', '0', '0', '0', '0']
                        for j in range(len(str(bin(i[1]))[2:])):
                            temp[-j-1] = str(bin(i[1]))[-j-1]
                        for i in temp:
                            give += i

                give_file.write(str(bin(lc))[2:] + '\t'+give+'\n')
                lc += 1
            else:

                validNonMRI = False
                for i in reg_Ref_list+io_Ref_list:
                    if code[instStr:instStr+3] == i:
                        validNonMRI = True
                        break

                if validNonMRI:

                    give = ''
                    if code[instStr:instStr+3] =='CLA':
                        give += '0111100000000000'
                    elif code[instStr:instStr+3] =='CLE':
                        give += '0111010000000000'
                    elif code[instStr:instStr+3] =='CMA':
                        give += '0111001000000000'
                    elif code[instStr:instStr+3] =='CME':
                        give += '0111000100000000'
                    elif code[instStr:instStr+3] =='CIR':
                        give += '0111000010000000'
                    elif code[instStr:instStr+3] =='CIL':
                        give += '0111000001000000'
                    elif code[instStr:instStr+3] =='INC':
                        give += '0111000000100000'
                    elif code[instStr:instStr+3] =='SPA':
                        give += '0111000000010000'
                    elif code[instStr:instStr+3] =='SNA':
                        give += '0111000000001000'
                    elif code[instStr:instStr+3] =='SZA':
                        give += '0111000000000100'
                    elif code[instStr:instStr+3] =='SZE':
                        give += '0111000000000010'
                    elif code[instStr:instStr+3] =='HLT':
                        give += '0111000000000001'
                    elif code[instStr:instStr+3] =='INP':
                        give += '1111100000000000'
                    elif code[instStr:instStr+3] =='OUT':
                        give += '1111010000000000'
                    elif code[instStr:instStr+3] =='SKI':
                        give += '1111001000000000'
                    elif code[instStr:instStr+3] =='SKO':
                        give += '1111000100000000'
                    elif code[instStr:instStr+3] =='ION':
                        give += '1111000010000000'
                    elif code[instStr:instStr+3] =='IOF':
                        give += '1111000001000000'
                    give_file.write(str(bin(lc))[2:] + '\t'+give+'\n')
                    lc += 1
                else:
                    print('Error :\t', lc)
                    lc += 1      

def twoscomplement(input_number):
    mask = 2**(1 + len(bin(input_number)[2:])) - 1      # Calculate mask to do bitwise XOR operation
    twos_comp = (input_number ^ mask) + 1               # calculate 2's complement, for negative of input_number (-1 * input_number)
    twos_comp=str(bin(twos_comp))
    twos_comp=twos_comp[2:]  
    return twos_comp      



memo_Ref_list = ["AND", "ADD", "LDA", "STA", "BUN", "BSA", "ISZ"]
reg_Ref_list = ["CLA", "CLE", "CMA", "CME", "CIR", "CIL","INC", "SPA", "SNA", "SZA", "SZE", "HLT"]
io_Ref_list = ["INP", "OUT", "SKI", "SKO", "ION", "IOF"]
pscode_list = ["ORG", "END", "DEC", "HEX"]

get_file=open('subtraction.asm','r')
test=get_file.readlines()

give_file=open("out.txt","w")

symbol_table=[]

fp()

get_file.close()
give_file.close()




                    





