package sem2.smai.project.test;

import java.io.FileNotFoundException;
import java.io.RandomAccessFile;

public class WriteTest {
	public static void main(String[] args) {
		try {
			RandomAccessFile r = new RandomAccessFile("/Users/adityagaykar/Downloads/Stackoverflow/Posts.xml", "rw");
			r.seek(0);		
			//r.writeUTF();
			r.writeBytes("<?xml version=\"1.0\" encoding=\"UTF-8\"?>   ");
			//r.seek(0);
			//r.writeUTF("<?xml version=\"1.0\" encoding=\"UTF-8\"?><p");
			r.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
