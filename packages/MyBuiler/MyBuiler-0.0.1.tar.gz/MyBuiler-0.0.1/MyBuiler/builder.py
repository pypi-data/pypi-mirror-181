class Builder:
	"""
	คลาส Builder คือ
	ข้อมูลที่เกี่ยวข้องกับ สร้าง
	ประกอบด้วยชื่อเพจ
	ชื่อยูทูป

	Example
	# -------------------
	build = Builder()
	build.show_name()
	build.page()
	build.show_youtube()
	build.about()
	build.show_art()
	# -------------------
	"""
	def __init__(self):
		self.name = "บิวเดอร์ สร้าง"
		self.page = 'https://www.facebook.com/Narawit.naprae'

	def show_page(self):
		print(f'FB page: {self.page}')

	def show_name(self):
		print(f'สวัสดีฉันชื่อ {self.name}')

	def show_youtube(self):
		print('https://www.youtube.com/')

	def about(self):
		text = """
		--------------------------------
		สวัสดีจ้า นี่คือสร้างเองเป็นผู้ที่รวยที่สุดในโลก
		สามารถติดตามทาง facebook ได้เลย	
		--------------------------------"""
		print(text)
	def show_art(self):
		text = """
		                          .
                          A       ;
                |   ,--,-/ \\---,-/|  ,
               _|\\,'. /|      /|   `/|-.
           \\`.'    /|      ,            `;.
          ,'\\   A     A         A   A _ /| `.;
        ,/  _              A       _  / _   /|  ;
       /\\  / \\   ,  ,           A  /    /     `/|
      /_| | _ \\         ,     ,             ,/  \
     // | |/ `.\\  ,-      ,       ,   ,/ ,/      \\/
     / @| |@  / /'   \\  \\      ,              >  /|    ,--.
    |\\_/   \\_/ /      |  |           ,  ,/        \\  ./' __:..
    |  __ __  |       |  | .--.  ,         >  >   |-'   /     `
  ,/| /  '  \\ |       |  |     \\      ,           |    /
 /  |<--.__,->|       |  | .    `.        >  >    /   (
/_,' \\  ^  /  \\     /  /   `.    >--            /^\\   |
      \\___/    \\   /  /      \\__'     \\   \\   \\/   \\  |
       `.   |/          ,  ,                  /`\\    \\  )
         \\  '  |/    ,       V    \\          /        `-\
          `|/  '  V      V           \\    \\.'            \\_
           '`-.       V       V        \\./'\
               `|/-.      \\ /   \\ /,---`\\         Build
                /   `._____V_____V'
                           '     '

		"""
		print(text)


if __name__ == '__main__':
	build = Builder()
	build.show_name()
	build.show_page()
	build.show_youtube()
	build.about()
	build.show_art()
