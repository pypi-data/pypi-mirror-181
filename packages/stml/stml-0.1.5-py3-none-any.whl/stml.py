def stml(input_file) :
 output_file=input_file.replace(".stml",".html")
 file1 =open(input_file,"r")
 file2 =open(output_file,"w")
 str,prev,exc="",0,0
 close_ind=[]
 close_tag=[]

 remove_list=['area','base','br','col','embed','hr','img',
             'input','keygen','link','meta','param','source','track','wbr']
 for j in file1:
  jj = j
  if jj.strip() != "" and jj[len(jj)-len(jj.lstrip())]!="#":
   str,cl1_ind,colon,c1,p,leadspace,colon_after,cl1,i_count ="",0,0,0,0,0,0,0,0
   close_ind1=[]
   for i in j:
    i_count+=1
    if i!="\n":
     if i ==" "and c1!=1:
         leadspace+=1
     else :
         c1=1
     if colon >0 and i !=" ":
         colon_after +=1
     if i==":":
         colon+=1
         if cl1!=1:
             cl1_ind=i_count
             cl1=1
         colon_after=0
     elif colon==0:
         str+=i
   if exc==1:
       jexc=j.replace("\n"," ")

   if cl1_ind!=0:
    j=j[0:cl1_ind-1]+j[cl1_ind:]
   else:
       j = j[0:cl1_ind ] + j[cl1_ind:]
       cl1_ind=0
   j=j.replace("\n","")
   str=str.strip()
   if colon==0 and exc!=1 :
      temt=j.lstrip()+"\n"
      file2.write(temt)
   for i in reversed(close_ind):
    close_ind1.append(i)
   for r in close_ind1:
      p+=1
      if close_ind[len(close_ind) - 1] == leadspace:
       exc = 0
      if r==leadspace:
          for y in range(p):
              p-=1
              if close_tag != []:
                  close_ind.pop()
                  temt = "</" + close_tag.pop() + ">"
                  file2.write(temt)
          break
   if colon ==1 and colon_after==0 and exc!=1:
      temt="<"+j.lstrip()+">\n"
      file2.write(temt)
      if str not in remove_list:
          close_tag.append(str)
          close_ind.append(leadspace)
   if colon >=1 and colon_after>0 and exc!=1:
      temt="<"+j.lstrip()+">\n"
      file2.write(temt)
      if str not in remove_list:
         close_ind.append(leadspace)
         close_tag.append(str)
   if exc==1:
       temt =  jexc.lstrip() + "\n"
       file2.write(temt)
   if str=="script" or str=="style":
       exc=1

 while close_tag!=[] :
     temt = "</" + close_tag.pop() + ">"
     file2.write(temt)
 print("Output Successfully Created as "+ output_file )