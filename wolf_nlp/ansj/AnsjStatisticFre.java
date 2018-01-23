import org.ansj.domain.Result;
import org.ansj.domain.Term;
import org.ansj.splitWord.analysis.ToAnalysis;
import java.util.*;
import java.io.*;


public class AnsjStatisticFre {
    private List<File> fileList = new ArrayList<File>();
    private Set<String> expectedNature = new HashSet<String>();
    private Map<String, Integer> word_freq = new HashMap<String, Integer>();
    private String result_file = new String();
    private String matrixs_file = new String();

    public int GetFileSize() {
      return this.fileList.size();
    }

    public int Init(String filePath, String res_file, String matrixs) {
      //遍历文件夹
      this.result_file = res_file;
      this.matrixs_file = matrixs;

      File dir = new File(filePath);
      File[] files = dir.listFiles(); // 该文件目录下文件全部放入数组
      if (files == null) {
        System.out.println("maybe dir not right");
        return 0;
      }

      for (int i = 0; i < files.length; i++) {
        String fileName = files[i].getName();
        if (files[i].isDirectory()) { // 判断是文件还是文件夹
          this.Init(files[i].getAbsolutePath(), this.result_file, this.matrixs_file); // 获取文件绝对路径
        } else { // 判断是否是文件
          if (files[i] != null) {
            fileList.add(files[i]);
          }
        }
      }

      //只关注这些词性的词
      this.expectedNature.add("n");
      this.expectedNature.add("v");
      this.expectedNature.add("vd");
      this.expectedNature.add("vn");
      this.expectedNature.add("vf");
      this.expectedNature.add("vx");
      this.expectedNature.add("vi");
      this.expectedNature.add("vl");
      this.expectedNature.add("vg");
      this.expectedNature.add("nt");
      this.expectedNature.add("nz");
      this.expectedNature.add("nw");
      this.expectedNature.add("nl");
      this.expectedNature.add("ng");
      this.expectedNature.add("userDefine");
      this.expectedNature.add("wh");

      return 1;
    }

    //分词
    public void start() {
        for (int i = 0; i < this.fileList.size(); i++) {
          BufferedReader reader = null;
          FileReader fr = null;
          try {
            fr = new FileReader(this.fileList.get(i).getAbsolutePath());
            reader = new BufferedReader(fr);

            System.out.println("start file " + this.fileList.get(i).getAbsolutePath());
            String temp_str = new String();
            Map<String, Integer> temp_word_freq = new HashMap<String, Integer>();
            while ((temp_str = reader.readLine()) != null) {
              List<Term> terms = ToAnalysis.parse(temp_str).getTerms();
              for(int j=0; j<terms.size(); j++) {
                if(this.expectedNature.contains(terms.get(j).getNatureStr())) {
                  if (this.word_freq.containsKey(terms.get(j).getName()) != false) {
                    int count = this.word_freq.get(terms.get(j).getName()) + 1;
                    this.word_freq.put(terms.get(j).getName(), count);
                  }
                  else {
                    this.word_freq.put(terms.get(j).getName(), 1);
                  }

                  if(temp_word_freq.containsKey(terms.get(j).getName()) != false) {
                    temp_word_freq.put(terms.get(j).getName(), temp_word_freq.get(terms.get(j).getName())+1);
                  }
                  else {
                    temp_word_freq.put(terms.get(j).getName(),1);
                  }
                }
              }
            }

            try {
              String new_file = this.fileList.get(i).getName() + ".ansjwords";
              new_file = this.fileList.get(i).getParent() + "/" + new_file;
              FileWriter tmp_fw = new FileWriter(new_file) ;
              BufferedWriter tmp_writer = new BufferedWriter(tmp_fw);
              for (Map.Entry<String, Integer> entry : temp_word_freq.entrySet()) {
                String key = entry.getKey().toString();
                int value = entry.getValue();
                tmp_writer.write(key + " " + value);
                tmp_writer.newLine();
                tmp_writer.flush();
              }
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

            System.out.println("word freq size " + this.word_freq.size());
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

        try {
          System.out.println("begin write result");
          FileWriter fw = new FileWriter(this.result_file);
          BufferedWriter bw = new BufferedWriter(fw);
          for (Map.Entry<String, Integer> entry : this.word_freq.entrySet()) {
            String key = entry.getKey().toString();
            int value = entry.getValue();
            bw.write(key + " " + value);
            bw.newLine();
            bw.flush();
          }
          fw.close();
          bw.close();
          System.out.println("write result end");
        } catch (Exception e) {
          System.out.println("write result err " + e.getMessage());
        }
      }

    public void transform_matrix() {
      try {
        FileWriter fw = new FileWriter(this.matrixs_file);
        BufferedWriter writer = new BufferedWriter(fw);

        for (int i = 0; i < this.fileList.size(); i++) {
          Map<String, Integer> temp_word_freq = new HashMap<String, Integer>();
          String new_file = this.fileList.get(i).getParent() + "/" + this.fileList.get(i).getName() + ".ansjwords";
          FileReader fr = new FileReader(new_file);
          BufferedReader reader = new BufferedReader(fr);
          String temp_str = new String();
          while ((temp_str = reader.readLine()) != null) {
            String[] retvals = temp_str.split(" ");
            if (retvals.length == 2) {
              temp_word_freq.put(retvals[0], Integer.parseInt(retvals[1]));
            }
          }
          List<Integer> matrixs = new ArrayList<Integer>();
          for (Map.Entry<String, Integer> entry : this.word_freq.entrySet()) {
            if (temp_word_freq.containsKey(entry.getKey().toString()) != false) {
              matrixs.add(entry.getValue());
            }
            else {
              matrixs.add(0);
            }
          }

          String results_data = new String();
          results_data = this.fileList.get(i).getName() + " ";
          for(Integer data : matrixs) {
            results_data += data;
            results_data += ",";
          }

          writer.write(results_data);
          writer.newLine();
          writer.flush();
        }
        fw.close();
        writer.close();
      }
      catch (Exception matrix_e) {
        System.out.println("matrix error " + matrix_e.getMessage());
      }
    }

    public static void main(String[] args) {
        AnsjStatisticFre fa = new AnsjStatisticFre();
        String file_path = "./data";
        String conf_file = "";
        String result_file = "result.data";
        String matrix_file = "matrixs.data";
        if (fa.Init(file_path, result_file, matrix_file) < 1) {
          System.out.println("init error " + file_path);
        }
        else {
          System.out.println("file list len " + fa.GetFileSize());
        }
        fa.start();
        fa.transform_matrix();
    }
}
