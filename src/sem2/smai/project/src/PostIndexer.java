package sem2.smai.project.src;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

public class PostIndexer {

	private Map<String, Map<TagHelper,TagHelper>> mapper;
	private int fileCount;
	private int postCount;
	private static final int POST_LIMIT =1000000;
	public PostIndexer(){
		fileCount = 1;
		postCount = 0;
		mapper = new HashMap<String, Map<TagHelper,TagHelper>>();
	}
	public void indexPosts(PostPOJO post){
		//System.out.println(postCount);
		Set<String> bodyTokens = post.getBodyTokens();
		Set<String> tagTokens = post.getTags();
		Map<TagHelper,TagHelper> tmp = null;
		for(String token : bodyTokens){
			if(mapper.containsKey(token)){
				tmp = mapper.get(token);				
			} else {
				tmp = new HashMap<TagHelper,TagHelper>();			
				mapper.put(token, tmp);				
			}
			for(String tag: tagTokens){
				TagHelper tagHelper = new TagHelper();
				tagHelper.setName(tag);
				if(tmp.containsKey(tagHelper)){				
					//System.out.println("contaings ...");
					TagHelper th = tmp.get((tagHelper));
					th.setFrequency(th.getFrequency() + 1);
				} else {
					//System.out.println("set ...");
					tagHelper.setFrequency(1);
					tmp.put(tagHelper,tagHelper);
				}						
			}
		}
		postCount ++;
		if(postCount % 10000 == 0)
			System.out.println(postCount);
		if(postCount == POST_LIMIT){
			printMapper();
			mapper.clear();
			postCount = 0;
		}
	}
	
	public static final Comparator<TagHelper> cmp = new Comparator<TagHelper>(){

		@Override
		public int compare(TagHelper o1, TagHelper o2) {
			if(o1.getFrequency() > o2.getFrequency())
				return -1;
			if(o1.getFrequency() < o2.getFrequency())
				return 1;
			
			return o1.getName().compareTo(o2.getName());
		}
		
	};
	
	void printRemainingPosts(){
		if(postCount != 0){
			printMapper();
			mapper.clear();
			postCount = 0;
		}
	}
	
	void printMapper(){
		try{
//			TagHelper ob = new TagHelper();
//			ob.setName("cello");
//			TagHelper ob1 = new TagHelper();
//			ob1.setName("cello");
			//System.out.println(ob.equals(ob1) + " " + (ob == ob1));
			PrintWriter pr= new PrintWriter(new BufferedWriter(new FileWriter("rsc/primary_"+fileCount+".in")));
			TreeSet<String> tokens = new TreeSet<String>(mapper.keySet());
			StringBuilder sb = new StringBuilder();
			for(String token : tokens){
				sb.append(token+":");
				TreeSet<TagHelper> tags = new TreeSet<TagHelper>(cmp);
				Map<TagHelper, TagHelper> tmp = mapper.get(token);
				tags.addAll(tmp.keySet());
				boolean flag = true;
				for(TagHelper tag : tags){
					if(flag){
						sb.append(tmp.get(tag).toString());
						flag = false;
					} else 
						sb.append(";"+tmp.get(tag).toString());
				}
				pr.println(sb.toString());
				sb = new StringBuilder();
			}
			fileCount ++;
			pr.close();
		} catch (Exception e){
			e.printStackTrace();
		}
	}
}
