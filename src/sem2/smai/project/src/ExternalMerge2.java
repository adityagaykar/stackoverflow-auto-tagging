package sem2.smai.project.src;

import static java.nio.file.StandardOpenOption.READ;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.ByteBuffer;
import java.nio.channels.SeekableByteChannel;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

public class ExternalMerge2 {
	private List<String> files;
	private List<SeekableByteChannel> sbc;
	private List<StringBuilder> sb;
	private List<Boolean> end;
	private ByteBuffer buff;
	private String encoding = System.getProperty("file.encoding");
	private PrintWriter primaryIndexWriter;
	private PrintWriter secondaryIndexWriter, ternaryIndexWriter;
	ExternalMerge2(){
		files = new ArrayList<String>();
		sbc = new ArrayList<SeekableByteChannel>();
		sb = new ArrayList<StringBuilder>();
		end = new ArrayList<Boolean>();
		 buff = ByteBuffer.allocate(128*(1<<10));
		 try {
			primaryIndexWriter = new PrintWriter(new BufferedWriter(new FileWriter("rsc/primary.in")));
			secondaryIndexWriter = new PrintWriter(new BufferedWriter(new FileWriter("rsc/secondary.in")));
			ternaryIndexWriter = new PrintWriter(new BufferedWriter(new FileWriter("rsc/ternary.in")));			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		 
	}

	public boolean allEmpty(){
		for(boolean b : end){
			if(!b)
				return false;
		}		
		return true;
	}
	
	public String getLine(BufferedReader br, int id){
		String tmp = null;
		try {
			tmp = br.readLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
		if(tmp == null)
		{
			end.set(id, true);
		}
		return tmp;
	}
	
	public String getLine(SeekableByteChannel sbc, StringBuilder br, int id){
		String tmp = null;
		int readCount = 0;
		int newLineIndex = br.indexOf("\n"); 
		if( newLineIndex != -1){
			tmp = br.substring(0, newLineIndex +1);
			br.delete(0, newLineIndex + 1);
		}
		else{
			buff.clear();				
			try {
				while((readCount = sbc.read(buff)) > 0){
					buff.flip();
					tmp = Charset.forName(encoding).decode(buff).toString();
					br.append(tmp);
					newLineIndex =br.indexOf("\n"); 
					if(newLineIndex != -1)
						break;
					buff.clear();
				}
			} catch (IOException e) {		
				e.printStackTrace();
			}
			if(newLineIndex != -1){
				tmp = br.substring(0, newLineIndex +1);
				br.delete(0, newLineIndex+1);
			} else {
				end.set(id, true);
			}			
		}							
		return tmp;
	}
	
	public List<TagHelper> makeList(String s,int dN){
		s = s.trim();
		List<TagHelper> pr = new LinkedList<TagHelper>();
		if(s.equals(""))
			return pr;
		String arr[] = s.split(";");		
		for(String str : arr){
			TagHelper pg = new TagHelper();	
			String arr2[] = str.split("\\|");
			pg.setName(arr2[0].trim());
			pg.setFrequency(Integer.parseInt(arr2[1].trim()));
			pr.add(pg);
		}
		return pr;
	}
	
	public void doMerge(){
		int len = files.size();		
		PriorityQueue<String> prq = new PriorityQueue<String>();		
		Map<String, List<Map<TagHelper, TagHelper>>> terms = new HashMap<String, List<Map<TagHelper, TagHelper>>>();
		
		List<Boolean> goNext = new ArrayList<Boolean>(len);
		List<Integer> in = new ArrayList<Integer>(len);
		for(int i = 0; i < len; i++){
			goNext.add(true);
			in.add(0);
		}
		Map<String, Set<Integer>> nextSetter = new HashMap<String, Set<Integer>>();
		long position = 0;
		long tupleLength = 0;
		long prevLength = 0;
		long terPosition = 0;
		long terPrevLength = 0;
		long terRowsLength = 0;
		long c = 0;
		StringBuilder priWriter = new StringBuilder();
		StringBuilder secWriter = new StringBuilder();
		String prevStr = "-1";
		while(!allEmpty()){			
			prevLength = position;
			for(int i = 0; i < len; i++){
				if(!end.get(i) && goNext.get(i)){
					String currLine = getLine(sbc.get(i), sb.get(i),i);
					if(currLine == null)
						continue;
					String arrx[] = currLine.split(":");
					
					if(terms.containsKey(arrx[0])){
						String section[] = {arrx[1]};
						List<Map<TagHelper, TagHelper>> ts = terms.get(arrx[0]);
						//ts.add(new TreeMap<TagHelper,TagHelper>(PostIndexer.cmp));
						
						int secId = 0;
						for(Map<TagHelper, TagHelper> p : ts){
							List<TagHelper> tmp = makeList(section[secId++], section.length);							
							for(TagHelper th : tmp){
								if(p.containsKey(th)){
									//System.out.println("contains ...");
									TagHelper tmp_th = p.get(th);
									tmp_th.setFrequency(tmp_th.getFrequency()+th.getFrequency());
								} else {									
									p.put(th, th);
								}
							}
						}									
						nextSetter.get(arrx[0]).add(i);
					} else {
						String section[] = {arrx[1]};
						List<Map<TagHelper, TagHelper>> ts = new LinkedList<Map<TagHelper, TagHelper>>();
						ts.add(new HashMap<TagHelper,TagHelper>());
						
						int secId = 0;
						for(Map<TagHelper, TagHelper> p : ts){
							List<TagHelper> tmp = makeList(section[secId++], section.length);							
							for(TagHelper th : tmp){
								if(p.containsKey(th)){
									//System.out.println("contains ...");
									TagHelper tmp_th = p.get(th);
									tmp_th.setFrequency(tmp_th.getFrequency()+th.getFrequency());
								} else {									
									p.put(th, th);
								}
							}
						}												
						prq.add(arrx[0]);						
						terms.put(arrx[0], ts);
						Set<Integer> x = new HashSet<Integer>();
						x.add(i);
						nextSetter.put(arrx[0], x);
					}
				}
			}
			
			if(terms.isEmpty())
				break;
			
			String entry = prq.poll();
			List<Map<TagHelper,TagHelper>> ts = terms.get(entry);
			terms.remove(entry);		
			StringBuilder row = new StringBuilder();
			Set<Integer> vals = nextSetter.get(entry);
			for(int i = 0; i < len; i++ ){
				if(vals.contains(i))
					goNext.set(i, true);
				else
					goNext.set(i, false);
			}
			vals.clear();
			nextSetter.remove(entry);			
			int limit = 0;
			boolean sectionFlag = true;
			for(Map<TagHelper,TagHelper> t : ts){				
				boolean first = true;
				TreeSet<TagHelper> keys = new TreeSet<TagHelper>(PostIndexer.cmp);
				keys.addAll(t.keySet());
				//Set<TagHelper> keys = t.keySet();
				for(TagHelper value: keys){
				//	System.out.println("Value1 : "+value1);
//					TagHelper value = t.get(value1);					
					//System.out.println("Value : "+value);
//					if(value == null)
//						continue;
					if(first){						
						first = false;
						row.append(value.toString());
					} else {
						row.append(";");
						row.append(value.toString());
					}			
					if(++limit == 2000)
						break;				
				}		
				//System.out.println("=====end======");
				t.clear();
			}
			ts.clear();
			tupleLength = position+row.length() - prevLength;
			String terPrint = entry+":"+position+";"+tupleLength;						
			String currStr = entry.length() > 2 ? entry.substring(0,3) : entry; 			
			if(prevStr.equals("-1")){
				prevStr = currStr;
			} else {				
				if ( currStr.compareTo(prevStr) > 0){					 
					ternaryIndexWriter.println(prevStr+":"+terPosition+";"+terRowsLength);
					terPosition += terPrevLength + terRowsLength;					
					prevStr = currStr;
					terRowsLength = 0;
				}
			}
			terRowsLength += terPrint.length()+1;			
			priWriter.append(row.toString()+"\n");
			secWriter.append(terPrint+"\n");
			if(priWriter.length() > 50*(1<<20)){
				primaryIndexWriter.print(priWriter.toString());
				priWriter = null;
				priWriter = new StringBuilder();
			}
			if(secWriter.length() > 50*(1<<20)){
				secondaryIndexWriter.print(secWriter.toString());
				secWriter = null;
				secWriter = new StringBuilder();
			}
			position += row.length()+1;
		}
		if(terRowsLength != 0)
			ternaryIndexWriter.println(prevStr+":"+terPosition+";"+terRowsLength);
		if(priWriter.length() > 0){
			primaryIndexWriter.print(priWriter.toString());
			priWriter = null;
		}
		if(secWriter.length() > 0){
			secondaryIndexWriter.print(secWriter.toString());
			secWriter = null;
		}
		primaryIndexWriter.close();
		secondaryIndexWriter.close();
		ternaryIndexWriter.close();		
	}
	
	public void readFiles(){
		try{
			FileInputStream fi = new FileInputStream("rsc/files.in");
			BufferedReader br = new BufferedReader(new InputStreamReader(fi));
			String tmp = null;
			while((tmp = br.readLine()) != null){
				files.add(tmp);
				Path file = Paths.get(tmp);
				SeekableByteChannel sbcTmp = Files.newByteChannel(file,EnumSet.of(READ));
				sb.add(new StringBuilder());
				sbc.add(sbcTmp);
				end.add(false);
			}
			br.close();
			fi.close();
		} catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		ExternalMerge2 ex = new ExternalMerge2();
		ex.readFiles();
		ex.doMerge();
	}

}
