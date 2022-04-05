using Microsoft.VisualBasic.FileIO;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PSAST.lib
{
    class Helpers
    {
        public static void WriteAstCSVHeader(OrderedDictionary vector, string outPath)
        {
            File.WriteAllText(outPath, GetASTCSVHeader(vector));
        }

        public static string GetASTCSVHeader(OrderedDictionary vector)
        {
            // helper that takes a RVO feature vector dictionary and uses that to write out a CSV header
            var csv = new StringBuilder();

            string[] items = new string[vector.Keys.Count];
            vector.Keys.CopyTo(items, 0);

            // still fucky with the headers, escaping ,'s ?
            string header = String.Join("\",\"", items);
            csv.Append("\"Path\",\"" + header + "\"");

            return csv.ToString();
        }

        public static void WriteAstVectorToCSV(string scriptPath, OrderedDictionary vector, string outPath)
        {
            scriptPath = scriptPath.Replace('\\', '/'); // for later Linux processing

            object[] temp = new object[vector.Values.Count];
            vector.Values.CopyTo(temp, 0);
            
            File.AppendAllText(outPath, $"\n\"{scriptPath}\",{String.Join(",", temp)}");
        }
    }
}
