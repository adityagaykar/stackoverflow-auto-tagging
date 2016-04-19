package sem2.smai.project.test;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

import sem2.smai.project.src.PostPOJO;
import sem2.smai.project.src.TagHelper;

public class RegexTest {
	private static final Pattern p = Pattern.compile("\\<.*?\\>",Pattern.MULTILINE);
	private static final Pattern p1 = Pattern.compile("\\<(.*?)\\>",Pattern.MULTILINE);
	
	public void test(PostPOJO post){
//		String body = p.matcher(post.getBody()).replaceAll("");
//		body = body.replaceAll("[^a-zA-Z0-9#+ ]", " ");
//		String body_arr[] = body.split(" ");
//		for(String s : body_arr){
//			System.out.println(s);
//		}
//		String tags = null;
//		Matcher m = p1.matcher(post.getTags());//.replaceAll("");
//		//System.out.println(body);
//		System.out.println("----------------\nTags\n----------------");
//		while(m.find()){
//			tags = m.group(1);
//			System.out.println(tags);
//		}
//		System.out.println("================");
	}
	
	public static void main(String[] args) {
		Map<TagHelper, TagHelper> m = new HashMap<TagHelper, TagHelper>();
		TagHelper th = new TagHelper();
		th.setName("c#");
		th.setFrequency(1);
		m.put(th, th);
		TagHelper th1 = new TagHelper();
		th1.setName("c#");
		System.out.println(m.containsKey(th1));
		System.out.println(th.equals(th1));
	}
}
/*
 &lt;p&gt;I want to use a track-bar to change a form's opacity.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;
 This is my code:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;
 decimal trans = trackBar1.Value / 5000;&#xA;this.Opacity = 
 trans;&#xA;&lt;/code&gt;&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;When I 
 try to build it, I get this error:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA; 
  &lt;p&gt;Cannot implicitly convert type 'decimal' to 'double'.&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;I 
  tried making &lt;code&gt;trans&lt;/code&gt; a &lt;code&gt;double&lt;/code&gt;, but then the control doesn't work. 
  This code has worked fine for me in VB.NET in the past. &lt;/p&gt;&#xA;
 
 */