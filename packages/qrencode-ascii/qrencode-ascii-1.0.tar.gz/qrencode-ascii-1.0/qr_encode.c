#include <Python.h>
#include <stdlib.h>
#include <qrencode.h>

#if PY_MAJOR_VERSION >= 3
#  define BYTES "y"
#else
#  define BYTES "s"
#endif

static int margin = 2;

static void writeUTF8_margin(FILE* fp, int realwidth, const char* white,
                             const char *reset, const char* full)
{
    int x, y;

    for (y = 0; y < margin/2; y++) {
        fputs(white, fp);
        for (x = 0; x < realwidth; x++)
            fputs(full, fp);
        fputs(reset, fp);
        fputc('\n', fp);
    }
}

static int writeUTF8_fp(const QRcode *qrcode, FILE *fp, int use_ansi, int invert)
{
    int x, y;
    int realwidth;
    const char *white, *reset;
    const char *empty, *lowhalf, *uphalf, *full;

    empty = " ";
    lowhalf = "\342\226\204";
    uphalf = "\342\226\200";
    full = "\342\226\210";

    if (invert) {
        const char *tmp;

        tmp = empty;
        empty = full;
        full = tmp;

        tmp = lowhalf;
        lowhalf = uphalf;
        uphalf = tmp;
    }

    if (use_ansi){
        if (use_ansi == 2) {
            white = "\033[38;5;231m\033[48;5;16m";
        } else {
            white = "\033[40;37;1m";
        }
        reset = "\033[0m";
    } else {
        white = "";
        reset = "";
    }

    realwidth = (qrcode->width + margin * 2);

    /* top margin */
    writeUTF8_margin(fp, realwidth, white, reset, full);

    /* data */
    for(y = 0; y < qrcode->width; y += 2) {
        unsigned char *row1, *row2;
        row1 = qrcode->data + y*qrcode->width;
        row2 = row1 + qrcode->width;

        fputs(white, fp);

        for (x = 0; x < margin; x++) {
            fputs(full, fp);
        }

        for (x = 0; x < qrcode->width; x++) {
            if(row1[x] & 1) {
                if(y < qrcode->width - 1 && row2[x] & 1) {
                    fputs(empty, fp);
                } else {
                    fputs(lowhalf, fp);
                }
            } else if(y < qrcode->width - 1 && row2[x] & 1) {
                fputs(uphalf, fp);
            } else {
                fputs(full, fp);
            }
        }

        for (x = 0; x < margin; x++)
            fputs(full, fp);

        fputs(reset, fp);
        fputc('\n', fp);
    }

    /* bottom margin */
    writeUTF8_margin(fp, realwidth, white, reset, full);

    fclose(fp);

    return 0;
}

static PyObject *encode(PyObject *self, PyObject *args)
{
    char *data;
    int version, level, hint, case_sensitive, fd;
    QRcode *code;

    if(!PyArg_ParseTuple(args, BYTES "iiiii:_qrencode.encode",
                         &data, &fd, &version, &level, &hint, &case_sensitive))
        return NULL;

    FILE *fp = fdopen(fd, "w");
    code = QRcode_encodeString(data, version, level, hint, case_sensitive);
    if (!code) {
        return Py_BuildValue("");
    }

    writeUTF8_fp(code, fp, 2, 0);
    QRcode_free(code);
    return Py_BuildValue("");;
};


static PyObject *encode_bytes(PyObject *self, PyObject *args)
{
    const unsigned char *data;
    int size, version, level, fd;
    QRcode *code;

    if(!PyArg_ParseTuple(args, BYTES "#iii:_qrencode.encode",
                         &data, &fd, &size, &version, &level))
        return NULL;

    FILE *fp = fdopen(fd, "w");
    code = QRcode_encodeData(size, data, version, level);
    if (!code) {
        return Py_BuildValue("");
    }

    writeUTF8_fp(code, fp, 2, 0);
    QRcode_free(code);
    return Py_BuildValue("");;
};

static PyMethodDef methods[] =
{
    {"encode", encode, METH_VARARGS, "Encodes a string as a QR-code. Returns a tuple of (version, width, data)"},
    {"encode_bytes", encode_bytes, METH_VARARGS, "Encodes raw bytes as a QR-code. Returns a tuple of (version, width, data)"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "qrencode._qrencode",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC
PyInit__qrencode(void)
{
    return PyModule_Create(&module);
}

#else

PyMODINIT_FUNC
init_qrencode(void)
{
    Py_InitModule("qrencode._qrencode", methods);
}

#endif
