#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <limits.h>

#include "c_hmerizer.h"

// This function sets a Python Exception based on the error codes recieved from main hashmerizer code.
static PyObject *raise_PyError(PMAF_CEXT_ERROR err_code)
{
    switch(err_code)
    {
        case ERR_PY_SOME_KMER_EXCEED:
            PyErr_SetString(PyExc_ValueError, "ERR_PY_SOME_KMER_EXCEED" );
            break;
        case ERR_PY_TOTAL_KMERS_EXCEED:
            PyErr_SetString(PyExc_ValueError, "ERR_PY_TOTAL_KMERS_EXCEED" );
            break;
        case ERR_MEMALC_RECORD_ELEMENT:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_RECORD_ELEMENT" );
            break;
        case ERR_MEMALC_AMBIGUOUS_MAP:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_AMBIGUOUS_MAP" );
            break;
        case ERR_MEMALC_HASHMASK:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_HASHMASK" );
            break;
        case ERR_MEMALC_DEAMBIG:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_DEAMBIG" );
            break;
        case ERR_MEMALC_HASHMERIZE:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_HASHMERIZE" );
            break;
        case ERR_MEMALC_PARSER_TOTAL:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_TOTAL" );
            break;
        case ERR_MEMALC_PARSER_HMER_ELEMENT:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_HMER_ELEMENT" );
            break;
        case ERR_MEMALC_THEORETICAL_PARSER:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_THEORETICAL_PARSER" );
            break;
        case ERR_MEMALC_PRIMER_ELEMENT:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PRIMER_ELEMENT" );
            break;
        case ERR_MEMALC_PRIMER_STATE_ELEMENT:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PRIMER_STATE_ELEMENT" );
            break;
                 
        case ERR_MEMALC_PARSER_AMBIGUOUS_CHUNK:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_AMBIGUOUS_CHUNK" );
            break;
        case ERR_MEMALC_PARSER_HASHMASK_CHUNK:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_HASHMASK_CHUNK" );
            break;
        case ERR_MEMALC_PARSER_HMER_CHUNK:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_HMER_CHUNK" );
            break;
        case ERR_MEMALC_PARSER_HMER_CHUNK_ELEM:
            PyErr_SetString(PyExc_MemoryError, "ERR_MEMALC_PARSER_HMER_CHUNK_ELEM" );
            break;


        case ERR_NO_ERROR:
            PyErr_SetString(PyExc_UserWarning, "ERR_NO_ERROR." );

    }
    return NULL;
}


// This is secondary function that is used externally from Python to test if requested kmer sizes are valid and will not cause any memory error.
// Memory allocation problems mainly depend on size_t datatype and SIZE_MAX; hence, it depends on how the C extension was compiled.
// To make most out of the C extension it is recommended to compile the code with -m64 bit parameter and provide necessary 64 bit header file locations.
PyObject *get_dtype_size_tuple(PyObject *self, PyObject *args)
{
    return PyTuple_Pack(4, PyLong_FromSize_t(sizeof(size_t)), PyLong_FromSize_t(SIZE_MAX), PyLong_FromSize_t(sizeof(HASH_INT)), PyLong_FromUnsignedLongLong(ULONG_MAX));
}

// This is helper function that makes PySet from parsed record element of type STRUCT_SEQ_HMER_ELEM
// This code was changed and I am currently not sure if Py_ssize_t is sufficiently large to contain corresponding size_t values.
// According to PEP 353 specification it should.
PyObject *make_PyTuple_from_hmer_element(STRUCT_SEQ_HMER_ELEM *hmer_element)
{
    Py_ssize_t hmer_i,hmer_total;
    PyObject *hmer_tuple;

    hmer_total = (Py_ssize_t)hmer_element->hmer_total;
    hmer_tuple = PyTuple_New(hmer_total);
    for(hmer_i = 0; hmer_i < hmer_total; hmer_i++)
    {   
        PyTuple_SET_ITEM(hmer_tuple,hmer_i, PyTuple_Pack(3,PyLong_FromUnsignedLongLong(hmer_element->hmer_pack_array[hmer_i].hmer), PyLong_FromUnsignedLong(hmer_element->hmer_pack_array[hmer_i].first_pos), PyLong_FromUnsignedLong(hmer_element->hmer_pack_array[hmer_i].last_pos)));
    }
    return hmer_tuple;
}

PyObject *make_PyTuple_from_record_primer_state_element(STRUCT_PRM_STATE_ELEM *primer_state_array,int total_primers)
{
    Py_ssize_t total_primer_i;
    PyObject *primer_state_PyDict;

    primer_state_PyDict = PyDict_New();
    for(total_primer_i = 0; total_primer_i < total_primers; total_primer_i++)
    {
        PyDict_SetItem(primer_state_PyDict,PyLong_FromUnsignedLong(primer_state_array[total_primer_i].primer_id),PyTuple_Pack(2,PyLong_FromUnsignedLong(primer_state_array[total_primer_i].primer_state),PyLong_FromUnsignedLong(primer_state_array[total_primer_i].primer_first_pos)));
    }
    return primer_state_PyDict;
}


// This is helper function that makes record element of STRUCT_SEQ_RECORD_ELEM type from incomming PyTuples.
PMAF_CEXT_ERROR make_record_element_from_PyTuples(STRUCT_SEQ_RECORD_ELEM **record_element, PyObject *record_element_PyTuple)
{
    unsigned long seq_id;
    char* seq_str;
    int seq_len;
    int seq_tab;
    PyArg_ParseTuple(record_element_PyTuple,"ksii",&seq_id,&seq_str,&seq_len,&seq_tab);
    return make_record_element(record_element, seq_id, seq_str, seq_len, seq_tab);
}

// This is main function and main interface to the Python.
// Function iterates over record generator from PyTuples and efficiently digests record and generates tuple of tuples with record id and hash values.
PyObject *parse_record_PyTupleGenerator(PyObject *record_PyGenerator,PyObject *kmer_sizes_PyTuple, PyObject *chunksize_PyLong)
{
    PMAF_CEXT_ERROR err_code;
    int kmer_size_total = (int)PyTuple_Size(kmer_sizes_PyTuple);
    Py_ssize_t chunksize = PyLong_AsSsize_t(chunksize_PyLong);
    Py_ssize_t chunksize_i;
    int *kmer_sizes;
    kmer_sizes = (int *)malloc(kmer_size_total*sizeof(int));
    int kmer_sizes_i;
    for (kmer_sizes_i = 0; kmer_sizes_i < kmer_size_total; kmer_sizes_i++)
    {
        kmer_sizes[kmer_sizes_i] = (int) PyLong_AsSsize_t(PyTuple_GetItem(kmer_sizes_PyTuple,(Py_ssize_t)kmer_sizes_i));
    }
    PyObject *record_PyIterator = PyObject_GetIter(record_PyGenerator);
    PyObject *record_element_PyTuple;
    PyObject *parsed_records_PyDict = PyDict_New();
    STRUCT_SEQ_RECORD_ELEM **record_element_chunk;
    STRUCT_SEQ_HMER_ELEM **parsed_record_chunk;
    record_element_chunk = (STRUCT_SEQ_RECORD_ELEM **)malloc(chunksize*sizeof(STRUCT_SEQ_RECORD_ELEM *));
    parsed_record_chunk = (STRUCT_SEQ_HMER_ELEM **)malloc(chunksize*sizeof(STRUCT_SEQ_HMER_ELEM *));
    chunksize_i = 0;
    while((record_element_PyTuple = PyIter_Next(record_PyIterator)))
    {
        err_code = make_record_element_from_PyTuples(&record_element_chunk[chunksize_i],record_element_PyTuple);
        if (err_code != ERR_NO_ERROR) { raise_PyError(err_code); free(record_element_chunk); free(parsed_record_chunk); return NULL; }
        
        Py_DECREF(record_element_PyTuple);
        chunksize_i++;
    }

    Py_DECREF(record_PyIterator);

    Py_BEGIN_ALLOW_THREADS; // Following block is multithreading. No GIL.

    err_code = parse_record_element_chunk(&parsed_record_chunk, record_element_chunk, kmer_sizes, kmer_size_total, chunksize);
   
    Py_END_ALLOW_THREADS; //Ending of non GIL block;

    if (err_code != ERR_NO_ERROR) { free(record_element_chunk); free(parsed_record_chunk); raise_PyError(err_code); return NULL; }

    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        PyDict_SetItem(parsed_records_PyDict,PyLong_FromUnsignedLong(parsed_record_chunk[chunksize_i]->seq_id),make_PyTuple_from_hmer_element(parsed_record_chunk[chunksize_i]));
    }

    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        free(record_element_chunk[chunksize_i]);
        free(parsed_record_chunk[chunksize_i]->hmer_pack_array);
        free(parsed_record_chunk[chunksize_i]);
    }

    free(record_element_chunk);
    free(parsed_record_chunk);
    free(kmer_sizes);

    return parsed_records_PyDict;
}

PyObject *parse_primers_for_records_chunk(PyObject *record_PyGenerator,PyObject *primer_records_PyTuple, PyObject *chunksize_PyLong)
{
    PMAF_CEXT_ERROR err_code;
    int total_primers = (int)PyTuple_Size(primer_records_PyTuple);
    int total_primers_i;
    Py_ssize_t chunksize = PyLong_AsSsize_t(chunksize_PyLong);
    Py_ssize_t chunksize_i;
    STRUCT_SEQ_RECORD_ELEM *record_element;
    STRUCT_PRM_RECORD_ELEM **primer_element_array;    
    PyObject *primer_record_element_PyTuple;
    primer_element_array = (STRUCT_PRM_RECORD_ELEM **)malloc(total_primers*sizeof(STRUCT_PRM_RECORD_ELEM*));
    for (total_primers_i = 0; total_primers_i < total_primers; total_primers_i++)
    {
        primer_record_element_PyTuple = PyTuple_GetItem(primer_records_PyTuple,(Py_ssize_t)total_primers_i);
        err_code = make_record_element_from_PyTuples(&record_element,primer_record_element_PyTuple);
        if (err_code != ERR_NO_ERROR) { raise_PyError(err_code); return NULL; }
        err_code = make_primer_element_from_record_element(&(primer_element_array[total_primers_i]),record_element);
        if (err_code != ERR_NO_ERROR) { raise_PyError(err_code); return NULL; }
    }
    PyObject *record_PyIterator = PyObject_GetIter(record_PyGenerator);
    PyObject *record_element_PyTuple;
    PyObject *parsed_records_PyDict = PyDict_New();
    STRUCT_SEQ_RECORD_ELEM **record_element_chunk;
    STRUCT_SEQ_PRM_STATE_ELEM *parsed_record_primer_state;
    STRUCT_SEQ_PRM_STATE_ELEM **parsed_record_primer_state_chunk;
    record_element_chunk = (STRUCT_SEQ_RECORD_ELEM **)malloc(chunksize*sizeof(STRUCT_SEQ_RECORD_ELEM *));
    parsed_record_primer_state_chunk = (STRUCT_SEQ_PRM_STATE_ELEM **)malloc(chunksize*sizeof(STRUCT_SEQ_PRM_STATE_ELEM *));
    chunksize_i = 0;
    while((record_element_PyTuple = PyIter_Next(record_PyIterator)))
    {
        err_code = make_record_element_from_PyTuples(&record_element,record_element_PyTuple);
        if (err_code != ERR_NO_ERROR) { raise_PyError(err_code); free(record_element_chunk); free(parsed_record_primer_state); return NULL; }
        record_element_chunk[chunksize_i] = record_element;
        
        Py_DECREF(record_element_PyTuple);
        chunksize_i++;
    }
    Py_DECREF(record_PyIterator);

    Py_BEGIN_ALLOW_THREADS; // Following block is multithreading. No GIL.
    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        err_code = run_primer_testing(&parsed_record_primer_state,primer_element_array,record_element_chunk[chunksize_i],total_primers);
        if (err_code != ERR_NO_ERROR) { break; }
        parsed_record_primer_state_chunk[chunksize_i] = parsed_record_primer_state;
    }
    Py_END_ALLOW_THREADS; //Ending of non GIL block;
    
    //return PyTuple_Pack(3,PyLong_FromUnsignedLongLong(parsed_record_primer_state_chunk[0]->seq_id),PyLong_FromUnsignedLongLong(parsed_record_primer_state_chunk[0]->primer_state_array->primer_id),PyLong_FromUnsignedLongLong((unsigned long long)parsed_record_primer_state_chunk[0]->primer_state_array->primer_state));
    if (err_code != ERR_NO_ERROR)
    {
        for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
        {
            free(record_element_chunk[chunksize_i]);
            free(parsed_record_primer_state_chunk[chunksize_i]);
        }
        free(record_element_chunk);
        free(parsed_record_primer_state);
        free(primer_element_array);
        raise_PyError(err_code);
        return NULL;
    }

    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        PyDict_SetItem(parsed_records_PyDict,PyLong_FromUnsignedLong(parsed_record_primer_state_chunk[chunksize_i]->seq_id),make_PyTuple_from_record_primer_state_element(parsed_record_primer_state_chunk[chunksize_i]->primer_state_array,total_primers));
    }

    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        free(record_element_chunk[chunksize_i]);
        free(parsed_record_primer_state_chunk[chunksize_i]);
    }

    free(record_element_chunk);
    free(parsed_record_primer_state_chunk);

    return parsed_records_PyDict;
}

PyObject *parse_theoretical_record_PyTupleGenerator(PyObject *record_PyGenerator,PyObject *kmer_size_PyLong, PyObject *chunksize_PyLong)
{
    PMAF_CEXT_ERROR err_code;
    Py_ssize_t chunksize = PyLong_AsSsize_t(chunksize_PyLong);
    Py_ssize_t chunksize_i;
    int sequence_len = (int)PyLong_AsLong(kmer_size_PyLong);

    PyObject *record_PyIterator = PyObject_GetIter(record_PyGenerator);
    char **sequence_array;
    PyObject *record_element_PyTuple;
    sequence_array = (char **)malloc(chunksize*sizeof(char *));
    PyObject *parsed_hash_PySet;
    parsed_hash_PySet = PySet_New(NULL);
    HASH_INT *parsed_hash_array;
    chunksize_i = 0;
    while((record_element_PyTuple = PyIter_Next(record_PyIterator)))
    {
        PyArg_ParseTuple(record_element_PyTuple,"s",&(sequence_array[chunksize_i]));
        Py_DECREF(record_element_PyTuple);

        chunksize_i++;
    }

    Py_DECREF(record_PyIterator);

    Py_BEGIN_ALLOW_THREADS; // Following block is multithreading. No GIL.

    err_code = parse_theoretical_record_elements(&parsed_hash_array,sequence_array,sequence_len, chunksize);
    if (err_code != ERR_NO_ERROR) { free(parsed_hash_array); return NULL; }

    Py_END_ALLOW_THREADS; //Ending of non GIL block;

    for(chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        PySet_Add(parsed_hash_PySet,PyLong_FromUnsignedLongLong(parsed_hash_array[chunksize_i]));
    }

    free(parsed_hash_array);

    return parsed_hash_PySet;
}

// This is wrapper function that parses METH_VARARGS type arguments from Python and passes into parse_record_PyTupleGenerator
// Not that Py_DECREF was not applied to created PyObjects. This is because PyArg_ParseTuple with "O" format actually does not create new object it just passes reference to the targets.
// Therefore, no reference count is increased and no need to decrease it. Python API willPy_XDECREF
PyObject *parse_records(PyObject *self, PyObject *args)
{
    PyObject *record_PyGenerator;
    PyObject *kmer_sizes_PyTuple;
    PyObject *chunksize_PyLong;
    PyArg_ParseTuple(args,"OOO",&record_PyGenerator,&kmer_sizes_PyTuple,&chunksize_PyLong);
    return parse_record_PyTupleGenerator(record_PyGenerator,kmer_sizes_PyTuple,chunksize_PyLong);//PyLong_FromUnsignedLongLong(5);
}

// This is wrapper function that parses METH_VARARGS type arguments from Python and passes into parse_record_PyTupleGenerator
PyObject *parse_theoretical_records(PyObject *self, PyObject *args)
{
    PyObject *record_PyGenerator;
    PyObject *kmer_size_PyLong;
    PyObject *chunksize_PyLong;

    PyArg_ParseTuple(args,"OOO",&record_PyGenerator,&kmer_size_PyLong,&chunksize_PyLong);
    return parse_theoretical_record_PyTupleGenerator(record_PyGenerator,kmer_size_PyLong,chunksize_PyLong);
}

PyObject *parse_records_for_primers(PyObject *self, PyObject *args)
{
    PyObject *record_PyGenerator;
    PyObject *primer_records_PyTuple;
    PyObject *chunksize_PyLong;

    PyArg_ParseTuple(args,"OOO",&record_PyGenerator,&primer_records_PyTuple,&chunksize_PyLong);
    return parse_primers_for_records_chunk(record_PyGenerator,primer_records_PyTuple,chunksize_PyLong);
}


// Following are self descriptive piece of code that tells Python that this is a cPython Extension.

static PyMethodDef PMAFCEXTMethods[] = {
    {"parse_record_chunk", parse_records, METH_VARARGS, "Hasmerizes each deambiguated kmer for every kmer size."},
    {"parse_theoretical_kmers_chunk", parse_theoretical_records, METH_VARARGS, "Fixed non-ambiguous kmer hashmerizer function for generating theoretical kmer hash values."},
    {"parse_match_primers_for_record_chunk", parse_records_for_primers, METH_VARARGS, "Deambiguate both primers and sequences to finds any matches of primers in records."},
    {"get_size_info", get_dtype_size_tuple, METH_NOARGS, "Secondary function for kmer size verification with Python interface for C hashmerizer."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef PMAFCEXTModule = {
    PyModuleDef_HEAD_INIT,
    "PMAFCEXT",
    NULL,
    -1,
    PMAFCEXTMethods
};

PyMODINIT_FUNC PyInit_PMAFCEXT(void) {
    return PyModule_Create(&PMAFCEXTModule);
}




