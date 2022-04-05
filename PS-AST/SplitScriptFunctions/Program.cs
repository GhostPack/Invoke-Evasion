using System;
using System.Collections.Generic;
using System.IO;
using System.Management.Automation;
using System.Management.Automation.Language;

namespace SplitScriptFunctions
{
    class Program
    {
        public static void Usage()
        {
            Console.WriteLine("\n  SplitFunctions.exe <script.ps1> <C:\\path\\to\\output\\folder\\>\n");
            Console.WriteLine("      Parses the AST of script.ps1 and outputs each function as a separate script in the output folder.");
        }

        static void Main(string[] args)
        {
            if (args.Length != 2)
            {
                Usage();
                return;
            }

            var scriptPath = args[0];
            var outputDir = args[1];

            if (File.Exists(scriptPath) && Directory.Exists(outputDir))
            {
                try
                {
                    Token[] temp = null;
                    ParseError[] temp2 = null;
                    ScriptBlockAst ast = Parser.ParseFile(scriptPath, out temp, out temp2);
                    IEnumerable<Ast> functionASTs = ast.FindAll(testAst => testAst is FunctionDefinitionAst, false);

                    int counter = 0;
                    foreach (Ast functionAst in functionASTs)
                    {
                        string functionFilePath = $"{outputDir}\\{scriptPath}_function_{counter}.ps1";
                        File.WriteAllText(functionFilePath, functionAst.ToString());
                        counter++;
                    }

                    Console.WriteLine($"\n[+] All functions written to '{outputDir}'\n");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"\n[X] Error: {e}\n");
                }
            }
            else
            {
                Usage();
                return;
            }
        }
    }
}
