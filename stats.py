import sys

no_lsm_syscalls = []	# syscalls with no LSM hooks
syscall_num_lsm_map = {}	# syscalls -> number of LSM hooks
lsm_stats = {}	# number of LSM hooks -> number of syscalls with that number of LSM hooks
weightedAPI = []	# the order of the system calls signifies the weighted importance of the system calls
unweightedAPI = []	# the order of the system calls signifies the unweighted importance of the system calls

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print '''
			usage: python stats.py <syshooks_file_path> <output_file_path>
			''' 
		exit(1)

	with open(sys.argv[1]) as f:
		for line in f:
			fields = line.split('\t')
			syscall = fields[0]
			lsm_list = fields[1]
			lsm_list = lsm_list.translate(None, '[]')
			lsm_list = lsm_list.translate(None, ' ')
			hooks = lsm_list.strip().split(',')
			if '' in hooks:
				hooks.remove('')
			hooks = list(set(hooks))
			print hooks
			if len(hooks) == 0:
				no_lsm_syscalls.append(syscall)
			else:
				syscall_num_lsm_map[syscall] = len(hooks)
				if len(hooks) not in lsm_stats:
					lsm_stats[len(hooks)] = 1
				else:
					lsm_stats[len(hooks)] = lsm_stats[len(hooks)] + 1
	f.close()

	skip_first_line = 0
	with open("weightAPI.txt", "r") as f:
		for line in f:
			if skip_first_line == 0:
				skip_first_line += 1
			else:
				fields = line.split("(")
				weightedAPI.append(fields[0])
	f.close()

	skip_first_line = 0
	with open("unweightAPI.txt", "r") as f:
		for line in f:
			if skip_first_line == 0:
				skip_first_line += 1
			else:
				fields = line.split("(")
				unweightedAPI.append(fields[0])
	f.close()

	with open(sys.argv[2], "w+") as f:
		f.write("Kernel Version: 4.16.8\n")
		f.write("Total number of system calls that trigger no LSM hooks: " + str(len(no_lsm_syscalls)) + "\n")
		f.write("Those system calls are:\n")
		for syscall in no_lsm_syscalls:
			f.write("\t" + syscall + '\n')
		f.write("==========Statistics of System Calls That Trigger LSM Hooks==========\n")
		f.write("SYSCALL NAME\t\t\t\t\t\t\t\t\tNUMBER OF HOOKS CALLED\n")
		for syscall in syscall_num_lsm_map:
			f.write(syscall + '\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[syscall]) + '\n')
		f.write("======================================================================\n\n")
		f.write("NUMBER OF HOOKS CALLED\t\t\t\t\t\tNUMBER OF SYSTEM CALLS\n")
		for num in lsm_stats:
			f.write(str(num) + '\t\t\t\t\t\t\t\t\t\t\t' + str(lsm_stats[num]) + '\n')
		f.write("======================================================================\n\n")
		f.write("WEIGHTED API CALL (MOST TO LEAST IMPORTANT)\t\t\tNUMBER OF HOOKS CALLED\n")
		for wsyscall in weightedAPI:
			SyS_syscall = "SyS_" + wsyscall
			sys_syscall = "sys_" + wsyscall
			C_SYSC_x86_syscall = "C_SYSC_x86_" + wsyscall
			C_SYSC_syscall = "C_SYSC_" + wsyscall
			if SyS_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[SyS_syscall]) + '\n')
			elif sys_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[sys_syscall]) + '\n')
			elif C_SYSC_x86_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[C_SYSC_x86_syscall]) + '\n')
			elif C_SYSC_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[C_SYSC_syscall]) + '\n')
			else:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + "N/A" + '\n')
		f.write("======================================================================\n\n")
		f.write("UNWEIGHTED API CALL (MOST TO LEAST IMPORTANT)\t\t\tNUMBER OF HOOKS CALLED\n")
		for wsyscall in unweightedAPI:
			SyS_syscall = "SyS_" + wsyscall
			sys_syscall = "sys_" + wsyscall
			C_SYSC_x86_syscall = "C_SYSC_x86_" + wsyscall
			C_SYSC_syscall = "C_SYSC_" + wsyscall
			if SyS_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[SyS_syscall]) + '\n')
			elif sys_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[sys_syscall]) + '\n')
			elif C_SYSC_x86_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[C_SYSC_x86_syscall]) + '\n')
			elif C_SYSC_syscall in syscall_num_lsm_map:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(syscall_num_lsm_map[C_SYSC_syscall]) + '\n')
			else:
				f.write(wsyscall + '\t\t\t\t\t\t\t\t\t\t\t\t\t' + "N/A" + '\n')
	f.close()
