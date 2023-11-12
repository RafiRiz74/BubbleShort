from mpi4py import MPI

def parallel_bubble_sort(data, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()
    local_data = data[rank::size]  # Pisahkan data menjadi bagian yang sama untuk setiap prosesor

    for _ in range(size):
        local_data = local_bubble_sort(local_data)  # Urutkan data lokal dengan Bubble Sort

        if rank % 2 == 0:
            if rank < size - 1:
                comm.send(local_data, dest=rank + 1)
                received_data = comm.recv(source=rank + 1)
                local_data = merge(local_data, received_data)
        else:
            if rank > 0:
                received_data = comm.recv(source=rank - 1)
                comm.send(local_data, dest=rank - 1)
                local_data = merge(local_data, received_data)

    return local_data

def local_bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return data

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        data = [5, 2, 9, 3, 1, 8, 6, 4, 7]
        sorted_data = parallel_bubble_sort(data, comm)
        print("Sorted Data:", sorted_data)
    else:
        parallel_bubble_sort([], comm)
