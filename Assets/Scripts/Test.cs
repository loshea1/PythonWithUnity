using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor.Scripting.Python;

public class Test : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // Set the Python interpreter path
        // PythonSettings.Instance.pythonInterpreter = "path/to/your/python";

        //path to python script
        string pythonScriptPath = Application.dataPath + "/Scripts/Python Scripts/GUI.py";

        //Run script
        PythonRunner.RunFile(pythonScriptPath);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
