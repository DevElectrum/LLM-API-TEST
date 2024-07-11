import java.io.*;
import java.util.Map;
import java.util.List;
import java.util.HashMap;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class SonarSeverityCalculator {
    public static void main(String[] args) {
        try {
            JSONParser parser = new JSONParser();
            FileReader reader = new FileReader("sample.json");
            JSONObject jsonData = (JSONObject) parser.parse(reader);

            JSONObject metricsComponent = (JSONObject) ((JSONObject) jsonData.get("metrics")).get("component");
            JSONArray measures = (JSONArray) metricsComponent.get("measures");

            List<String> metrics = List.of(
                "complexity", "minor_violations", "duplicated_lines_density", "duplicated_lines", "functions", 
                "new_vulnerabilities", "security_remediation_effort", "classes", "sqale_index", "blocker_violations", 
                "bugs", "lines_to_cover", "major_violations", "new_violations", "ncloc", "reliability_remediation_effort", 
                "line_coverage", "lines", "coverage", "reliability_rating", "code_smells", "new_lines", "security_rating", 
                "violations", "sqale_debt_ratio", "comment_lines_density", "new_bugs", "critical_violations", 
                "new_code_smells", "info_violations", "comment_lines", "uncovered_lines", "duplicated_blocks", 
                "files", "vulnerabilities", "file_complexity"
            );

            List<Double> values = new ArrayList<>();
            List<Integer> weights = new ArrayList<>();

            double w_value = 0;
            double m_value = 0;

            Map<String, Integer> weightsMap = new HashMap<>() {{
                put("ncloc", 1); put("lines", 1); put("files", 2); put("functions", 2); put("classes", 2);
                put("complexity", 3); put("file_complexity", 3);
                put("comment_lines", 1); put("comment_lines_density", 1);
                put("duplicated_lines", 4); put("duplicated_blocks", 4); put("duplicated_lines_density", 4);
                put("violations", 5); put("blocker_violations", 6); put("critical_violations", 5); put("major_violations", 4);
                put("minor_violations", 2); put("info_violations", 1);
                put("code_smells", 3); put("sqale_index", 5); put("sqale_debt_ratio", 4);
                put("bugs", 6); put("reliability_rating", 5); put("reliability_remediation_effort", 4);
                put("vulnerabilities", 6); put("security_rating", 5); put("security_remediation_effort", 4);
                put("coverage", 5); put("line_coverage", 5);
                put("lines_to_cover", 3); put("uncovered_lines", 4);
                put("new_lines", 1); put("new_violations", 5); put("new_bugs", 6); put("new_vulnerabilities", 6); put("new_code_smells", 3);
                put("alert_status", 5);
            }};

            Map<String, Double> metricsMaxValues = new HashMap<>() {{
                put("complexity", 200.0);
                put("minor_violations", 50.0);
                put("duplicated_lines_density", 10.0);
                put("duplicated_lines", 1000.0);
                put("functions", 1500.0);
                put("new_vulnerabilities", 20.0);
                put("security_remediation_effort", 72.0);
                put("classes", 1000.0);
                put("sqale_index", 500.0);
                put("blocker_violations", 10.0);
                put("bugs", 20.0);
                put("lines_to_cover", 5000.0);
                put("major_violations", 20.0);
                put("new_violations", 20.0);
                put("ncloc", 5000.0);
                put("reliability_remediation_effort", 120.0);
                put("line_coverage", 100.0);
                put("lines", 20000.0);
                put("coverage", 100.0);
                put("reliability_rating", 5.0);
                put("code_smells", 500.0);
                put("new_lines", 1000.0);
                put("security_rating", 5.0);
                put("violations", 150.0);
                put("sqale_debt_ratio", 20.0);
                put("comment_lines_density", 50.0);
                put("new_bugs", 20.0);
                put("critical_violations", 10.0);
                put("new_code_smells", 50.0);
                put("info_violations", 20.0);
                put("comment_lines", 5000.0);
                put("uncovered_lines", 1000.0);
                put("duplicated_blocks", 200.0);
                put("files", 500.0);
                put("vulnerabilities", 50.0);
                put("file_complexity", 100.0);
            }};

            for (Object obj : measures) {
                JSONObject measure = (JSONObject) obj;
                String metric = (String) measure.get("metric");
                if (metric.equals("alert_status")) {
                    continue;
                }

                if (List.of("new_lines", "new_bugs", "new_vulnerabilities", "new_violations", "new_code_smells").contains(metric)) {
                    JSONArray periods = (JSONArray) measure.get("periods");
                    JSONObject period = (JSONObject) periods.get(0);
                    values.add(Double.parseDouble(period.get("value").toString()));
                    weights.add(weightsMap.get(metric));
                } else {
                    values.add(Double.parseDouble(measure.get("value").toString()));
                    weights.add(weightsMap.get(metric));
                }
            }

            for (int j = 0; j < weights.size(); j++) {
                w_value += weights.get(j) * values.get(j);
                m_value += weights.get(j) * metricsMaxValues.get(metrics.get(j));
            }

            System.out.println(w_value + " " + m_value);

            double sonar_severity = (w_value / m_value) * 1000;

            System.out.println(sonar_severity);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
