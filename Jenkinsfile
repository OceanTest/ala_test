#!/usr/bin/env groovy

import org.jenkinsci.plugins.pipeline.utility.steps.fs.FileWrapper
import com.cwctravel.hudson.plugins.extended_choice_parameter.ExtendedChoiceParameterDefinition
import java.net.URLEncoder
import java.util.regex.Matcher
import groovy.transform.Field
import javax.ws.rs.core.UriBuilder
import groovy.xml.*
import static java.util.UUID.randomUUID

def slave1Config = [
    "0" : ['SSH_ID': env.SOC1_0_SSH_ID,'APC_IP': env.SOC1_0_APC_IP,  'APC_SLOT': env.SOC1_0_APC_SLOT,'TARGET_IP': env.SOC1_0_TARGET_IP,'TCP_IP':env.SOC1_0_TCP_IP],
    "1" : ['SSH_ID': env.SOC1_1_SSH_ID,'APC_IP': env.SOC1_1_APC_IP,  'APC_SLOT': env.SOC1_1_APC_SLOT,'TARGET_IP': env.SOC1_1_TARGET_IP,'TCP_IP':env.SOC1_1_TCP_IP]
]
def slave2Config = [
    "0" : ['SSH_ID': env.SOC2_0_SSH_ID,'APC_IP': env.SOC2_0_APC_IP,  'APC_SLOT': env.SOC2_0_APC_SLOT,'TARGET_IP': env.SOC2_0_TARGET_IP,'TCP_IP':env.SOC2_0_TCP_IP],
    "1" : ['SSH_ID': env.SOC2_1_SSH_ID,'APC_IP': env.SOC2_1_APC_IP,  'APC_SLOT': env.SOC2_1_APC_SLOT,'TARGET_IP': env.SOC2_1_TARGET_IP,'TCP_IP':env.SOC2_1_TCP_IP],
    "2" : ['SSH_ID': env.SOC2_2_SSH_ID,'APC_IP': env.SOC2_2_APC_IP,  'APC_SLOT': env.SOC2_2_APC_SLOT,'TARGET_IP': env.SOC2_2_TARGET_IP,'TCP_IP':env.SOC2_2_TCP_IP]
]
def configMap = [ (env.SOC1_SLAVENAME) : slave1Config, (env.SOC2_SLAVENAME) : slave2Config]

def toDo = [
    /* Build with tests */
    //[ name: '1098R20_Internal_E2e_Bics2_Nvme',              soc: '1098R20',  customer: 'Internal',      target: 'E2e_Bics2_Nvme',                configId: '0',  build: 'windows-build', test: env.SOC2_SLAVENAME],

    /* Build only */
    //Eldora
    /* [ name: '1093R21_Internal_E2e_tfx132',           soc: '1093R21',         customer: 'Internal',      target: 'E2e_tfx132',                    configId: '0',  build: 'windows-build' ],
    [ name: '1093R21_Internal_E2e_tfx132_Mst',       soc: '1093R21',         customer: 'Internal',      target: 'E2e_tfx132_Mst',                configId: '0',  build: 'windows-build' ],
    //Zao
    [ name: '1098_Internal_E2e_Bics2_Nvme',                soc: '1098',      customer: 'Internal',      target: 'E2e_Bics2_Nvme',                configId: '0',  build: 'windows-build'],
    [ name: '1098_Internal_E2e_Bics3_Nvme',                soc: '1098',      customer: 'Internal',      target: 'E2e_Bics3_Nvme',                configId: '0',  build: 'windows-build' ],
    [ name: '1098_Internal_E2e_Bics2_Nvme_4MediaSpaces',   soc: '1098',      customer: 'Internal',      target: 'E2e_Bics2_Nvme_4MediaSpaces',   configId: '0',  build: 'windows-build' ],
    [ name: '1098_Internal_E2e_Bics2_Nvme_Historylog',     soc: '1098',      customer: 'Internal',      target: 'E2e_Bics2_Nvme_Historylog',     configId: '0',  build: 'windows-build' ],
    [ name: '1098_Standard_E2e_Bics2',                     soc: '1098',      customer: 'Standard',      target: 'E2e_Bics2',                     configId: '0',  build: 'windows-build' ],


    //ZaoR20
    [ name: '1098R20_Internal_E2e_Bics2_Nvme_4MediaSpaces', soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics2_Nvme_4MediaSpaces',  configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Internal_E2e_Bics2_Nvme_Historylog',   soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics2_Nvme_Historylog',    configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Internal_E2e_Bics2_Sata',              soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics2_Sata',               configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Internal_E2e_Bics3_Nvme',              soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics3_Nvme',               configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Internal_Bics2_Nvme_Mst_Lite',         soc: '1098R20',      customer: 'Internal',     target: 'Bics2_Nvme_Mst_Lite',          configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Internal_E2e_Bics2_Nvme_Mst',          soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics2_Nvme_Mst',           configId: '0',   build: 'windows-build' ],
    [ name: '1098R20_Standard_Ramdrive0',                   soc: '1098R20',      customer: 'Standard',     target: 'Ramdrive0',                    configId: '0',   build: 'windows-build' ],*/
    [ name: '1098R20_Standard_E2e_Bics2_SC',                soc: '1098R20',      customer: 'Standard',     target: 'E2e_Bics2',                    configId: '0',   build: 'windows-build', test: env.SOC2_SLAVENAME ],
    [ name: '1098R20_Internal_E2e_Bics2_TP',                soc: '1098R20',      customer: 'Internal',     target: 'E2e_Bics2_Nvme',               configId: '1',   build: 'windows-build', test: env.SOC2_SLAVENAME ],
]

def stageCases = [
    // Test Case
    "FIO": [passedParser: this.&jsonTypePassedParser],
    "marvo": [passedParser: this.&jsonTypePassedParser]   
]
def testcases = ["FIO", "marvo"]
    
def testTasks = [:]

toDo.each { task ->
    testTasks["$task.name"] = {
        node("ocean_linuxnode") {           
            withEnv( //add variable into environment
                ["SSH_ID=${configMap[task.test][task.configId]['SSH_ID']}",
                "TCP_IP=${configMap[task.test][task.configId]['TCP_IP']}"]){                         
                echo "SSH_ID is ${SSH_ID}"
                echo "TCP_IP is ${TCP_IP}"              
                def results = [:]
                testcases.each { test ->
                    def settings = stageCases[test]
                    try{
                        // Run the different testing.
                        stage("${test} testing ${task.name}"){
                            switch (test) {
                                case "FIO":
                                    timeout(time: 3, unit: 'MINUTES') {
                                        sh script: "ssh ${SSH_ID} 'cd /home/svt/fio_script; python3 fio.py fio_test.ini tcp://${TCP_IP} marvell'"
                                    }
                                    sh script: "scp -r ${SSH_ID}:/home/svt/fio_script/Logs/FIO/ ${WORKSPACE}"
                                    sh script: "ssh ${SSH_ID} 'rm -r /home/svt/fio_script/Logs/FIO'"
                                    break
                                case "marvo":
                                    timeout(time: 3, unit: 'HOURS') {
                                        sh script: "ssh ${SSH_ID} 'cd /home/svt/marvo; xvfb-run -a python3 Marvo.py /home/svt/marvo /home/svt/marvo/PCIe tcp://${TCP_IP} marvell'"
                                    }
                                    sh script: "scp -r ${SSH_ID}:/home/svt/marvo/Logs/marvo ${WORKSPACE}"
                                    sh script: "ssh ${SSH_ID} 'rm -r /home/svt/marvo/Logs/marvo'"
                                    break
                            }
                        }                    
                        // Collect all test results as a map 
                        Map currentTestResults = [
                            (task.name): collectTestResults(                    
                                test,
                                settings.passedParser,
                                task.name,
                                )
                            ]
                           
                        results << currentTestResults    
                        //echo "results is ${results}"
                        writeFile(file: 'test.xml', text: resultsAsJUnit(currentTestResults))
                        // Generate the Junit Report 
                        //archiveArtifacts(artifacts: '${test}.xml', excludes: null)
                        step([
                            $class: 'JUnitResultArchiver',
                            testResults: '**/test.xml'
                            ])                    
                    } catch(e) {
                            /* Error Handling
                               When test is failed, upload the log onto Jenkins server.                            
                            */
                            echo "Testing failed due to $e"
                            switch (test) {
                                case "FIO":
                                    sh script: "scp -r ${SSH_ID}:/home/svt/fio_script/Logs/FIO/ ${WORKSPACE}"
                                    sh script: "ssh ${SSH_ID} 'rm -r /home/svt/fio_script/Logs/FIO'"
                                    break
                                case "marvo":
                                    sh script: "scp -r ${SSH_ID}:/home/svt/marvo/Logs/marvo ${WORKSPACE}"
                                    sh script: "ssh ${SSH_ID} 'rm -r /home/svt/marvo/Logs/marvo'"
                                    break
                            }
                            sh script: "tar -zPcv -f ${test}.tar.gz ${test}/*.log"
                            // Store the zips as a tar file
                            archiveArtifacts artifacts: "${test}.tar.gz", allowEmptyArchive: true
                            // Cleanup
                            sh "rm -rf ${test}/ ${test}.tar.gz"                            
                            currentBuild.description = """<br /><a style="text-decoration: none; background-color:red; color:white" href="${env.BUILD_URL}artifact/${test}_${TestName}.tar.gz"><b>Test failed: ${test}</b></a>"""
                        }finally {
                            // If there is no error, upload the test result table.    
                            // Publish the result table on the status overview.       
                            currentBuild.description = currentBuild.description + "<br /></strong>${resultsAsTable(results, test)}"                                
                            
                        } 
                }
            }                 
        }
    }
}        
          
timestamps {
    stage("Build") {
        echo "After Build"
        currentBuild.description = "<strong><a href='${env.BUILD_URL}/flowGraphTable/'>View logs per step</a></strong>"      
    }
    stage("Test") {
        parallel testTasks
    }
}

/**
 * Return the collected test result from every test case.
 * @param test The test means the different stage.
 * @param passedParser The function is used to check the selected file whether it includes required keyword. 
 */
def collectTestResults(String test, Closure passedParser, String Testname) {
    String copyPath = "$env.ARTIFACTS_COPY_PATH"    
    
    // Initialize empty result map.
    def resultMap = [:]

    // Gather all the logfiles produced.    
    def logFiles = sh (
            script: "ls ${test}/summary.log",
            returnStdout:true
            ).readLines()

    // Extract the test name and result from each logfile.    
    logFiles.each { logFile ->
        passedParser(logFile, resultMap)
    }

    sh script: "tar -zPcv -f ${test}_${Testname}.tar.gz ${test}/*.log"
    // Store the zips as a tar file
    archiveArtifacts artifacts: "${test}_${Testname}.tar.gz", allowEmptyArchive: true

    // Cleanup
    sh "rm -rf ${test}/ ${test}_${Testname}.tar.gz"

    // Return the accumulated result.
    return resultMap
}

/**
 * Return the collected test result is stored as a map from every test case. 
 * Parser for test results.
 * @param logFile The logFile means the different stage.
 * @param resultMap The resultMap is a map, recording the required file exists. 
 */

def jsonTypePassedParser(logFile, resultMap) {   
    String  testName
    boolean testPassed 
    readFile(logFile).split("\n").each { line ->
        testName = line.subSequence(0,line.lastIndexOf(":"))   
        testPassed = line.contains("Pass")
        resultMap << [(testName): testPassed]
        println resultMap
    }    
    return resultMap  
}
/**
 * Return the generated table based on different testcases and transferred to html format.
 * @param testResults The testResults means the result is stored as a map and aims to display on the jenkins. 
 */
 
@NonCPS
String resultsAsTable(def testResults, String testCase) {
    StringWriter  stringWriter  = new StringWriter()
    MarkupBuilder markupBuilder = new MarkupBuilder(stringWriter)

    // All those delegate calls here are messing up the elegancy of the MarkupBuilder
    // but are needed due to https://issues.jenkins-ci.org/browse/JENKINS-32766
    markupBuilder.html {
        delegate.body {
            delegate.style(".passed { color: #468847; background-color: #dff0d8; border-color: #d6e9c6; } .failed { color: #b94a48; background-color: #f2dede; border-color: #eed3d7; }", type: 'text/css')
            delegate.table {                
                testResults.each { test, testResult ->
                        delegate.delegate.tr {                            
                            delegate.td {
                                delegate.strong("[Stage] ${test}")
                                delegate.a("Logs", href: "${env.BUILD_URL}/artifact/${testCase}_${test}.tar.gz")
                                echo "testname is ${testCase}_${test}"
                            }
                        }
                        testResult.each { testName, testPassed ->
                            delegate.delegate.delegate.tr {
                                delegate.td("$testName", class: testPassed ? 'passed' : 'failed')
                            }
                        }
                    }
                
            }
        }
    }
    return stringWriter.toString()
}

/**
 * Return the generated xml format report based on different testcases.
 * @param testResults The testResults means the result is stored as a map and aims to display on the jenkins. 
 */

@NonCPS
String resultsAsJUnit(def testResults) {
    StringWriter  stringWriter  = new StringWriter()
    MarkupBuilder markupBuilder = new MarkupBuilder(stringWriter)
    // All those delegate calls here are messing up the elegancy of the MarkupBuilder
    // but are needed due to https://issues.jenkins-ci.org/browse/JENKINS-32766
    markupBuilder.testsuites {
        testResults.each{ test, testresult ->
            delegate.delegate.testsuite(name: testresult.testName, tests: testresult.size(), failures: testresult.values().count(false)) {
                testresult.each{ testName, testPassed ->
                    delegate.delegate.testcase(name: testName) {
                        if(!testPassed){
                            echo "${testResults.testPassed}"
                            delegate.failure()
                        }
                    }
                }
            }
        }
    }  
  return stringWriter.toString()
}