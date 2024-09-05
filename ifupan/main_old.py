# main.py

import text_analysis
import mind_map_generator
import speech_to_text

def main():
    print("欢迎使用AI智能复盘系统")
    while True:
        print("\n请选择功能:")
        print("1. 文字交互复盘")
        print("2. 思维导图形式展示")
        print("3. 语音交互复盘")
        print("4. 退出")
        
        choice = input("请输入选项(1-4): ")
        
        if choice == '1':
            text = input("请输入要复盘的文字: ")
            result = text_analysis.analyze(text)
            print("复盘结果:", result)
        
        elif choice == '2':
            text = input("请输入要生成思维导图的内容: ")
            mind_map = mind_map_generator.generate(text)
            print("思维导图已生成:", mind_map)
        
        elif choice == '3':
            print("请开始语音输入...")
            audio = speech_to_text.record_audio()
            text = speech_to_text.transcribe(audio)
            result = text_analysis.analyze(text)
            print("语音复盘结果:", result)
        
        elif choice == '4':
            print("感谢使用,再见!")
            break
        
        else:
            print("无效选项,请重新选择")

if __name__ == "__main__":
    main()
