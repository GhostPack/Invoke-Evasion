using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Management.Automation.Language;
using System.IO;
using System.Collections;
using System.Collections.Specialized;
using Microsoft.VisualBasic.FileIO;
using PSAST.lib;
using System.Threading;
using RGiesecke.DllExport;
using System.Runtime.InteropServices;

namespace PSAST
{
    class Program
    {
        public static void Usage()
        {
            Console.WriteLine("\n  PS-AST.exe <labeled_data.csv> <C:\\path\\to\\corpus\\folder\\>");
            Console.WriteLine("      Takes a .csv of 'script_path,label' and a PowerShellCorpus folder,");
            Console.WriteLine("      Processes all specified scripts and generates a corpus AST .csv");

            Console.WriteLine("\n  PS-AST.exe <single_script.ps1>\n");
            Console.WriteLine("      Generates a AST .csv for a single PowerShell script");
        }

        [DllExport("GetASTFile", CallingConvention = CallingConvention.Cdecl)]
        public static string GetASTFile(string scriptPath)
        {
            if (!File.Exists(scriptPath))
            {
                return "";
            }
            else
            {
                // get the RVO feature vector
                var vector = RevokeObfuscationHelpers.GetRvoFeatureVector(scriptPath, "1");

                string output = Helpers.GetASTCSVHeader(vector) + "\n";

                scriptPath = scriptPath.Replace('\\', '/'); // for later Linux processing
                object[] temp = new object[vector.Values.Count];
                vector.Values.CopyTo(temp, 0);

                output += $"\"{scriptPath}\",{String.Join(",", temp)}";

                return output;
            }
        }

        [DllExport("GetAST", CallingConvention = CallingConvention.Cdecl)]
        public static string GetAST(string inputScript)
        {
            // get the RVO feature vector
            var vector = RevokeObfuscationHelpers.GetRvoFeatureVector(inputScript, "1");

            // add in the header
            string output = Helpers.GetASTCSVHeader(vector) + "\n";

            object[] temp = new object[vector.Values.Count];
            vector.Values.CopyTo(temp, 0);

            output += $"\"script\",{String.Join(",", temp)}";

            return output;
        }

 
        static void Main(string[] args)
        {
            if(args.Length == 1)
            {
                var scriptPath = args[0];

                var astFile = $"{scriptPath}.ast.csv";

                if (!File.Exists(scriptPath))
                {
                    Console.WriteLine($"[!] File {scriptPath} doesn't exist!");
                    return;
                }

                // get the RVO feature vector
                var vector = RevokeObfuscationHelpers.GetRvoFeatureVector(scriptPath, "1");

                Helpers.WriteAstCSVHeader(vector, astFile);

                // write out the feature vector
                Helpers.WriteAstVectorToCSV(scriptPath, vector, astFile);
            }
            else if(args.Length == 2)
            {
                string dirName = "";
                string astFile = "";
                string dataLabels = args[0];

                if (args[1] == "-q")
                {
                    var scriptPath = args[0];

                    if (!File.Exists(scriptPath))
                    {
                        Console.WriteLine($"[!] File {scriptPath} doesn't exist!");
                        return;
                    }

                    // get the RVO feature vector
                    var vector = RevokeObfuscationHelpers.GetRvoFeatureVector(scriptPath, "1");

                    // write out the CSV header to stdout
                    Console.WriteLine(Helpers.GetASTCSVHeader(vector));

                    scriptPath = scriptPath.Replace('\\', '/'); // for later Linux processing
                    object[] temp = new object[vector.Values.Count];
                    vector.Values.CopyTo(temp, 0);

                    Console.WriteLine($"\"{scriptPath}\",{String.Join(",", temp)}");
                }
                else
                {
                    string corpusDirectory = args[1];

                    // ensure the inputs exist
                    if (File.Exists(dataLabels) && Directory.Exists(corpusDirectory))
                    {
                        var command = args[1];
                        dirName = new DirectoryInfo(corpusDirectory).Name;

                        // the output file will be the directory name of the corpus folder
                        astFile = $"{dirName}.ast.csv";
                    }
                    else
                    {
                        Usage();
                        return;
                    }

                    var watch = System.Diagnostics.Stopwatch.StartNew();
                    bool astHeaderWritten = false;
                    var fileCounter = 1;
                    Console.WriteLine("\n[*] Starting script processing...\n");

                    // parse the existing .csv containing Path,Label
                    using (TextFieldParser parser = new TextFieldParser(dataLabels))
                    {
                        parser.TextFieldType = FieldType.Delimited;
                        parser.SetDelimiters(",");
                        while (!parser.EndOfData)
                        {
                            if ((fileCounter % 1000) == 0)
                            {
                                Console.WriteLine($"[*] {fileCounter} files processed in {watch.ElapsedMilliseconds / 1000.0} seconds");
                            }

                            string[] fields = parser.ReadFields();
                            if (fields[0] == "Path")
                            {
                                continue;
                            }

                            var scriptPath = $"{corpusDirectory}\\{fields[0]}";
                            var label = fields[1];

                            // get the RVO feature vector
                            var vector = RevokeObfuscationHelpers.GetRvoFeatureVector(scriptPath, label);

                            // write the AST vector out if needed
                            if (!astHeaderWritten)
                            {
                                Helpers.WriteAstCSVHeader(vector, astFile);
                                astHeaderWritten = true;
                            }

                            // write out the feature vector
                            Helpers.WriteAstVectorToCSV(scriptPath, vector, astFile);

                            fileCounter++;
                        }
                    }

                    Console.WriteLine($"\n[*] Completed parsing {fileCounter} files processed from {corpusDirectory} in {watch.ElapsedMilliseconds / 1000.0} seconds");
                    Console.WriteLine($"\n[*] Feature .csv output at: {astFile}\n");
                }
            }
            else
            {
                Usage();
            }
        }
    }
}
