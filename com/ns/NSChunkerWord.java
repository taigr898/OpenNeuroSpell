package com.ns;

public class NSChunkerWord {
	public String word = null;
	public String lemma = null;
	public String pos = null;
	public String tag = null;
	
	public NSChunkerWord clone() {
		NSChunkerWord aW = new NSChunkerWord();
		aW.word = word;
		aW.lemma = lemma;
		aW.pos = pos;
		aW.tag = tag;
		return aW;
	}
}
