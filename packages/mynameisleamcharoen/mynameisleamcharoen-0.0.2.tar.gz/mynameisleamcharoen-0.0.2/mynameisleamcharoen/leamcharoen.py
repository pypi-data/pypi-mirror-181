class LaemCharoen:
    '''
    คลาส LeamCharoen คือ
    ข้อมูลที่เกี่ยวข้องกับ LaemCharoen
    ประกอบด้วยเพจ Facebook

    Example
    #---------------------------------------
    laem = LaemCharoen()
    laem.show_name()
    laem.show_page()
    laem.show_youtube()
    laem.about()
    laem.show_art()
    #---------------------------------------
    '''

    def __init__(self):
        self.name = 'แหลม เจริญ'
        self.page =  'https://www.facebook.com/jaroenchai.rodboon'

    def show_name(self):
        print('สวัสดีฉันชื่อ{}'.format(self.name))

    def show_page(self):
        print('Facebook : {}'.format(self.page))

    def show_youtube(self):
        print('YOUTUBE : https://www.youtube.com/watch?v=jKZXtJ31r_A')

    def about(self):
        text = '''
        -----------------------------------------------
        สวัสดีครับ ผม แหลม เป็นผุ้ดูแลเพจ jaroenchai rodboon
        สามารถเพิ่มเพื่อนและติดตามได้เลยครับ
        -----------------------------------------------
        '''
        print(text)

    def show_art(self):
        text = '''
                 _
                |.|
                ]^[
              ,-|||~\\
             {<|||||>}
              \|||||/
              {/   \}
              /__9__\\
              | / \ |
              (<   >)
             _|)   (|_
        ,.,.(  |.,.|  ).,.,.
        '''
        print(text)


if __name__ == '__main__':
    laem = LaemCharoen()
    laem.show_name()
    laem.show_page()
    laem.show_youtube()
    laem.about()
    laem.show_art()
   