package sem2.smai.project.src;




import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;


public class FeatureMapper {
	private static final Pattern p = Pattern.compile("\\<.*?\\>",Pattern.MULTILINE);
	private static final Pattern p1 = Pattern.compile("\\<(.*?)\\>",Pattern.MULTILINE);
	private List<String> features;
	private int c;
	private Set<String> tags;
	public FeatureMapper(){
		//postIndexer = new PostIndexer();
		tags = new HashSet<String>();
		features = new ArrayList<String>();		
	}
	
	public void readFeatures(String filepath){
		try{
			FileInputStream fis = new FileInputStream(filepath);
			BufferedReader br = new BufferedReader(new InputStreamReader(fis));
			String tmp;
			while((tmp = br.readLine()) != null){
				features.add(tmp.trim());
			}
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	
	public void init_parser(String filepath, String ouputFilePath, String startStr, String limitStr){
		try{
			c = 0;
			int start = Integer.parseInt(startStr);
			int limit= Integer.parseInt(limitStr);
			PrintWriter prx = new PrintWriter(ouputFilePath);
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
					if(qName.equals("row")){
						String postTypeId = attributes.getValue("PostTypeId");
						if(postTypeId.equals("1")){
							Set<String> bodyTokens = new HashSet<String>();
							Set<String> tagTokens = new HashSet<String>();
							String body = attributes.getValue("Title"); // changing to titles
							String tags = attributes.getValue("Tags");
							body = body.toLowerCase();
							tags = tags.toLowerCase();
							PostPOJO post = new PostPOJO();
							body = p.matcher(body).replaceAll("");
							body = body.replaceAll("[^a-zA-Z0-9#+@ ]", " ");
							String body_arr[] = body.split(" ");
							for(String s : body_arr){
								if(s.length() > 0){
									bodyTokens.add(s);
								}
							}							
							Matcher m = p1.matcher(tags);							
							String tmp = null;
							String tagStr = "";
							boolean hasTag = false;
							while(m.find()){
								tmp = m.group(1);
								if( tmp.length() > 0){
									tagTokens.add(tmp);
									if(tags.contains(tmp))
										hasTag = true;
								}
							}		
							tagStr = String.join("|", tagTokens);
							post.setBodyTokens(bodyTokens);
							post.setTags(tagTokens);
							List<Integer> featureIndex =new ArrayList<Integer>();
							for(String s : bodyTokens){
								int tmp1 = Collections.binarySearch(features, s);
								if(tmp1 >= 0 && tmp1 < features.size() && features.get(tmp1).equals(s))
									featureIndex.add(tmp1);
							}
							Collections.sort(featureIndex);
							List<String> featureList = new ArrayList<String>();
							for(int i = 0; i < features.size(); i++){
								int tmp1 = Collections.binarySearch(featureIndex, i);
								if(tmp1 >= 0 && tmp1 < featureIndex.size() && featureIndex.get(tmp1) == i )
									featureList.add("1");
								else
									featureList.add("0");
							}
							if(hasTag){
								if ( c > start)
									prx.println(String.join(":", featureList)+"#@#"+tagStr);
								c++;
								if(c > (start+limit)){
									prx.close();
									System.exit(0);
								}
							}
							
								
							
							//postIndexer.indexPosts(post);
//								RegexTest rt = new RegexTest();
//								rt.test(post);
						}
						builder = null;
						buffer = null;
					}
					
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
  	     // postIndexer.printRemainingPosts();
		} catch(Exception e){
			e.printStackTrace();
		}
		

	}
	public void readTags(String filepath){
		try{
			BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(filepath)));
			String tmp;
			while((tmp = br.readLine()) != null)
				tags.add(tmp.split("\\|")[0].trim());
			br.close();
		}catch(Exception e){			
			e.printStackTrace();
		}
		
	}
	public static void main(String[] args) {
		if(args.length < 1 ){
			System.out.println("Invalid args: pass xml file path as argument");
			System.exit(0);
		}
		FeatureMapper p = new FeatureMapper();
		p.readFeatures(args[4]);
		System.out.println("Started : "+new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date()));
		p.init_parser(args[0], args[1], args[2], args[3]);
		System.out.println("Ended : "+new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS").format(new Date()));
	}
}



