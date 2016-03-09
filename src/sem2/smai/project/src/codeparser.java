package sem2.smai.project.src;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;



public class codeparser {
	private static final Pattern p = Pattern.compile("\\<.*?\\>",Pattern.MULTILINE);
	private static final Pattern p1 = Pattern.compile("\\<(.*?)\\>",Pattern.MULTILINE);
	private Pattern codepattern=Pattern.compile("\\<code\\>(.*?)code\\>",Pattern.DOTALL);
	Matcher codematcher=null;
	private int c;
	public int count=0;
	PrintWriter out=null;
	private PostIndexer postIndexer;
	//public XMLParser(){
		//postIndexer = new PostIndexer();
	//}
	public codeparser()
	{
		try
			{
				out = new PrintWriter(new BufferedWriter(new FileWriter("codeindex.txt")));
				//out1=new PrintWriter(new BufferedWriter(new FileWriter("title.txt", true)));
			}
			catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		postIndexer = new PostIndexer();
	}

	public void init_parser(String filepath){
		try{
			c = 0;
			//out = new PrintWriter(new BufferedWriter(new FileWriter("codeindex.txt")));
			SAXParserFactory spf = SAXParserFactory.newInstance();
			SAXParser sp = spf.newSAXParser();
			DefaultHandler df = new DefaultHandler(){				
			StringBuilder builder = null;
			String buffer, post = null;
				@Override
				public void startDocument() throws SAXException {
					// TODO Auto-generated method stub
					//System.out.println("Parsing started");										
				}

				@Override
				public void endDocument() throws SAXException {
					// TODO Auto-generated method stub					
					//System.out.println("Parsing ended");
				}

				@Override
				public void startElement(String uri, String localName, String qName, Attributes attributes)
						throws SAXException {
					// TODO Auto-generated method stub
					try
			{
				out = new PrintWriter(new BufferedWriter(new FileWriter("codeindex.txt",true)));
				//out1=new PrintWriter(new BufferedWriter(new FileWriter("title.txt", true)));
			}
			catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
					//out.write("hello");
					//if (out!=null)
					//	System.out.println("hell");
					if(qName.equals("row")){
					//	if (count>100)
					//		System.exit(0);
					//	count++;
						Integer id = Integer.parseInt(attributes.getValue("Id"));
						String postTypeId = attributes.getValue("PostTypeId");
						if(postTypeId.equals("1")){
							Set<String> bodyTokens = new HashSet<String>();
							Set<String> tagTokens = new HashSet<String>();
							String body = attributes.getValue("Body"); // changing to titles
							String tags = attributes.getValue("Tags");
							body = body.toLowerCase();
							tags = tags.toLowerCase();
							PostPOJO post = new PostPOJO();
							codematcher=codepattern.matcher(body);

//							if (codematcher.find())
				    		  {
				    		  	//out.write(id+codematcher.group(0)+tags+"\n");
							String tmp = null;
							while(codematcher.find()){
								tmp = codematcher.group(1);
								if( tmp.length() > 0){
									String body_arr[] = tmp.split(" ");		
									for(String s : body_arr){
										if(s.length() > 0){
										bodyTokens.add(s);
										}
	
									}
								}
							}
							//out.write("hi");
				    		  	//	body=refmatcher.group(0);
				    		  }	

						/*	body = p.matcher(body).replaceAll("");
							body = body.replaceAll("[^a-zA-Z0-9#+@ ]", " ");
							String body_arr[] = body.split(" ");
							for(String s : body_arr){
								if(s.length() > 0){
									bodyTokens.add(s);
								}
							}							
							*/Matcher m = p1.matcher(tags);							
							String tmp = null;
							while(m.find()){
								tmp = m.group(1);
								if( tmp.length() > 0){
									tagTokens.add(tmp);
								}
							}		
							post.setBodyTokens(bodyTokens);
							post.setTags(tagTokens);
							postIndexer.indexPosts(post);
//							RegexTest rt = new RegexTest();
//							rt.test(post);
						}
						builder = null;
						buffer = null;
					}
						out.close();
					
				}
				
				
				@Override
				public void endElement(String uri, String localName, String qName) throws SAXException {
					// TODO Auto-generated method stub
					
				}

				@Override
				public void characters(char[] ch, int start, int length) throws SAXException {
					// TODO Auto-generated method stub
					//
					if(builder != null)
						builder.append(new String(ch, start,length));
					
				}
				
			};
		  InputStream inputStream= new FileInputStream(filepath);
		  
  	      Reader reader = new InputStreamReader(inputStream,"UTF-8");  	      
  	      InputSource is = new InputSource(reader);
  	      is.setEncoding("UTF-8");  	      //
  	      sp.parse(is, df);  
  	      postIndexer.printRemainingPosts();
		} catch(Exception e){
			e.printStackTrace();
		}
		

	}
	public static void main(String[] args) {
		if(args.length < 1 ){
			System.out.println("Invalid args: pass xml file path as argument");
			System.exit(0);
		}
		//XMLParser p = new XMLParser();
		codeparser p=new codeparser();
		System.out.println("Started : "+new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date()));
		p.init_parser(args[0]);
		System.out.println("Ended : "+new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date()));
	}
}


