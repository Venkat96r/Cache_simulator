import math

class CacheLine:
    def __init__(self):
        self.valid=False
        self.tag=None

class SetAssociativeCache:
    def __init__(self,cache_size_kb,block_size,associativity):
        num_blocks=(cache_size_kb * 1024) // block_size
        self.num_sets=num_blocks // associativity
        self.index_bits=int(math.log2(self.num_sets))
        self.block_offset_bits=int(math.log2(block_size)) 
        self.associativity=associativity
        self.cache=[[CacheLine() for _ in range(associativity)] for _ in range(self.num_sets)]
        self.lru=[[0 for _ in range(associativity)] for _ in range(self.num_sets)]

    def access(self,address):
        index=(address >> self.block_offset_bits) & ((1 << self.index_bits)-1)
        tag=address >> (self.index_bits+self.block_offset_bits)

        set_lines=self.cache[index]
        lru_counters=self.lru[index]

        for i in range(self.associativity):
            if set_lines[i].valid and set_lines[i].tagtag:
                lru_counters[i]=max(lru_counters)+1
                return True

        lru_min_index=lru_counters.index(min(lru_counters))
        set_lines[lru_min_index].valid=True
        set_lines[lru_min_index].tag=tag
        lru_counters[lru_min_index]=max(lru_counters)+1
        return False

def Run_Cache_Model(cache_size_kb,block_size,associativity,trace_file_path):
    cache=SetAssociativeCache(cache_size_kb,block_size,associativity)
    hits,misses=0,0
    with open(trace_file_path,'r') as trace_file:
        for line in trace_file:
            parts=line.strip().split()
            address=int(parts[1],16)  
            if cache.access(address):
                hits += 1
            else:
                misses += 1

    return hits,misses

for trace in ['gcc','swim','mcf','gzip','twolf']: 
    trace_file_path=f"{trace}.trace"  
    hits,misses=Run_Cache_Model(1024,4,4,trace_file_path)
    print(f"-----------------{trace}.trace--------------------")
    print(f"Part (a)-Cache Size: 1024 KB,Block Size: 4 Bytes,Associativity: 4-way")
    print(f"Hits: {hits},Misses: {misses},Hit Rate: {(hits / (hits+misses))*100},Miss Rate: {(misses/ (hits+misses))*100}")

    cache_sizes_kb=[128,256,512,1024,2048,4096]
    results=[]

    for cache_size_kb in cache_sizes_kb:
        hits,misses=Run_Cache_Model(cache_size_kb,4,4,trace_file_path)
        results.append((cache_size_kb,hits,misses))

    print("Part (b)-Varying Cache Size")
    for cache_size_kb,hits,misses in results:
        print(f"Cache Size: {cache_size_kb} KB,Hits: {hits},Misses: {misses},Hit Rate: {(hits / (hits+misses))*100},Miss Rate: {(misses/ (hits+misses))*100}")
    block_sizes=[1,2,4,8,16,32,64,128]
    results=[]

    for block_size in block_sizes:
        hits,misses=Run_Cache_Model(1024,block_size,4,trace_file_path)
        results.append((block_size,hits,misses))

    print("Part (c)-Varying Block Size")
    for block_size,hits,misses in results:
        print(f"Block Size: {block_size} Bytes,Hits: {hits},Misses: {misses},Hit Rate: {(hits / (hits+misses))*100},Miss Rate: {(misses/ (hits+misses))*100}")
    associativities=[1,2,4,8,16,32,64]
    results=[]

    for associativity in associativities:
        hits,misses=Run_Cache_Model(1024,4,associativity,trace_file_path)
        results.append((associativity,hits,misses))

    print("Part (d)-Varying Associativity")
    for associativity,hits,misses in results:
        print(f"Associativity: {associativity}-way,Hits: {hits},Misses: {misses},Hit Rate: {(hits / (hits+misses))*100},Miss Rate: {(misses/ (hits+misses))*100}")

