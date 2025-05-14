#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <time.h>
#include <unistd.h>

// === TIME_BASED ===
// == LOW ==
void localGetTime() {
  time_t start = time(NULL);

  for (int i = 0; i < 10; i++) {
    int random = rand();
    random = (random << 1) | (random >> 31);
  }

  time_t end = time(NULL);

  if (end - start > 1) {
    int value = 0;
    while (1) {
      value ^= rand();
      value = (value << 1) | (value >> 31);
      usleep(50000);
    }
  }
}

// == LOW ==
void clock_getTime() {
  struct timespec time_before, time_after;

  clock_gettime(0, &time_before);

  for (int i = 0; i < 10; i++) {
    int random = rand();
    random = (random << 1) | (random >> 31);
  }

  clock_gettime(0, &time_after);

  double elapsed_time = (time_after.tv_sec - time_before.tv_sec) +
                        (time_after.tv_nsec - time_before.tv_nsec) / 1e9;

  if (elapsed_time > 0.2) {
    int value = 0;
    while (1) {
      value ^= rand();
      value = (value << 1) | (value >> 31);
      usleep(50000);
    }
  }
}

// === PROCESS_SCAN_BASED ===
// == MEDIUM ==
void ptraceTraceme() {
  if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1) {
    int index = 0;
    char buffer[256] = {0};
    while (1) {
      buffer[index % 256] = rand() % 256;
      index = (index * 17 + 5) % 1024;
      for (int i = 0; i < 10; i++) {
        buffer[i] ^= buffer[(i + index) % 256];
      }
      usleep(10000);
    }
  } else {
    ptrace(PTRACE_DETACH, 0, 0, 0);
  }
}

// == HIGH ==
void parentProcessScan() {
  char path[256] = {0};
  size_t buffer_size = 256;
  ssize_t path_len = 0;
  int is_debugger = 0;
  char *exe_path = calloc(buffer_size, sizeof(char));
  if (exe_path) {

    int parent_pid = getppid();
    snprintf(path, sizeof(path) - 1, "/proc/%u/exe", parent_pid);

    while ((path_len = readlink(path, exe_path, buffer_size)) == buffer_size) {
      buffer_size *= 2;
      exe_path = realloc(exe_path, buffer_size);
      if (!exe_path) {
        break;
      }
      memset(exe_path, 0, buffer_size);
    }

    if (!strcmp(basename(exe_path), "gdb") || strstr(exe_path, "lldb") ||
        !strcmp(basename(exe_path), "strace") ||
        !strcmp(basename(exe_path), "ltrace")) {
      is_debugger = 1;
    }

    if (is_debugger) {
      int entropy = 42;
      while (1) {
        char data[128];
        for (int i = 0; i < sizeof(data); i++) {
          data[i] = (char)(rand() % 256);
          entropy ^= data[i];
          entropy = (entropy << 2) | (entropy >> 30);
        }
        volatile int dummy = entropy;
        (void)dummy;
        usleep(50000);
      }
    }

    free(exe_path);
  }
}
// == LOW ==
void tracerPidZero() {
  FILE *status_file = fopen("/proc/self/status", "r");
  if (!status_file == NULL) {
    char line[256];
    int tracer_pid = -1;

    while (fgets(line, sizeof(line), status_file)) {
      if (strncmp(line, "TracerPid:", strlen("TracerPid:")) == 0) {
        sscanf(line + strlen("TracerPid:"), "%d", &tracer_pid);
        break;
      }
    }

    fclose(status_file);

    if (tracer_pid == 0) {
      int entropy = 0;
      while (1) {
        entropy ^= rand();
        entropy = (entropy << 2) | (entropy >> 30);
        usleep(50000);
      }
    }
  }
}

// === MEMORY_BASED ===
// == MEDIUM ==
void nearHeap() {
  unsigned char stack_var;
  unsigned char *heap_ptr = malloc(0x10);

  if (heap_ptr - &stack_var <= 0x20000) {
    int entropy = 123;
    while (1) {
      entropy += rand() % 100;
      entropy = ((entropy << 4) & 0xFFFF) ^ (entropy >> 3);
      entropy ^= 0xA5A5;
      for (int i = 0; i < 3; ++i) {
        entropy ^= rand();
      }
      usleep(50000);
    }
  }
}
