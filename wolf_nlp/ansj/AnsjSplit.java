import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;
import java.util.*;
import java.io.*;


public class AnsjSplit {
    private List<File> fileList = new ArrayList<File>();
    private Set<String> expectedNature = new HashSet<String>();
    private Map<String, Integer> word_freq = new HashMap<String, Integer>();
    private List<String> splitWordList = new ArrayList<String>();
    private String result_file = new String();
    private String matrixs_file = new String();
    private String result_path = new String();

    public int GetFileSize() {
      return this.fileList.size();
    }

    public int Init(String filePath, String resPath) {
      //遍历文件夹
      this.result_path = resPath;
      File tmp_dir = new File(resPath);
      if (!tmp_dir.exists()) {
        if (tmp_dir.mkdirs()){
          System.out.println("create dir suceess " + resPath);
        }
      }

      File dir = new File(filePath);
      File[] files = dir.listFiles(); // 该文件目录下文件全部放入数组
      if (files == null) {
        System.out.println("maybe dir not right");
        return 0;
      }

      for (int i = 0; i < files.length; i++) {
        String fileName = files[i].getName();
        if (files[i].isDirectory()) { // 判断是文件还是文件夹
          this.Init(files[i].getAbsolutePath(), this.result_path); // 获取文件绝对路径
        } else { // 判断是否是文件
          if (files[i] != null) {
            fileList.add(files[i]);
          }
        }
      }

      this.expectedNature.add("w");
      this.expectedNature.add("wkz");
      this.expectedNature.add("wky");
      this.expectedNature.add("wyz");
      this.expectedNature.add("wyy");
      this.expectedNature.add("wj");
      this.expectedNature.add("ww");
      this.expectedNature.add("wt");
      this.expectedNature.add("wd");
      this.expectedNature.add("wf");
      this.expectedNature.add("wn");
      this.expectedNature.add("wm");
      this.expectedNature.add("ws");
      this.expectedNature.add("wp");
      this.expectedNature.add("wb");
      this.expectedNature.add("wh");
      this.expectedNature.add("null");
      return 1;
    }

    //分词
    public void start() {
        for (int i = 0; i < this.fileList.size(); i++) {
          BufferedReader reader = null;
          FileReader fr = null;
          this.splitWordList.clear();
          try {
            fr = new FileReader(this.fileList.get(i).getAbsolutePath());
            reader = new BufferedReader(fr);

            System.out.println("start file " + this.fileList.get(i).getAbsolutePath());
            String temp_str = new String();
            while ((temp_str = reader.readLine()) != null) {
              temp_str = temp_str.trim();
              List<Term> terms = ToAnalysis.parse(temp_str).getTerms();
              for(int j=0; j<terms.size(); j++) {
                String naturestr = terms.get(j).getNatureStr();
                if (naturestr != null && naturestr.length() > 0 && !this.expectedNature.contains(terms.get(j).getNatureStr())) {
                  this.splitWordList.add(terms.get(j).getName().trim());
                  //System.out.println(terms.get(j).getName()+":"+naturestr);
                }
              }
            }

            try {
              String new_file = this.fileList.get(i).getName() + ".ansjwords";
              new_file = this.result_path + "/" + new_file;
              FileWriter tmp_fw = new FileWriter(new_file) ;
              BufferedWriter tmp_writer = new BufferedWriter(tmp_fw);
              for (int index = 0; index < this.splitWordList.size(); index++){
                tmp_writer.write(this.splitWordList.get(index));
                tmp_writer.newLine();
              }
              tmp_writer.flush();
              tmp_fw.close();
              tmp_writer.close();
            }
            catch (Exception te) {
              System.out.println("write error" + te.getMessage());
            }
            if (fr != null && reader != null) {
              fr.close();
              reader.close();
            }
          } catch (Exception e) {
            System.out.println("first " + e.getMessage());
            if (fr != null && reader != null) {
              try {
                fr.close();
                reader.close();
              }
              catch (Exception ioe) {
                System.out.println("second " + ioe.getMessage());
              }
            }
            continue;
          }
        }
      }

    public static void main(String[] args) {
        AnsjSplit fa = new AnsjSplit();
        String file_path = "./data";
        String conf_file = "";
        String result_file = "result.data";
        String result_path = "./result.path";
        if (fa.Init(file_path, result_path) < 1) {
          System.out.println("init error " + file_path);
        }
        else {
          System.out.println("file list len " + fa.GetFileSize());
        }
        fa.start();
    }
}
