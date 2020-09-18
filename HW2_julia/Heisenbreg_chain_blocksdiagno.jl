#= Createn By WJM in Sep.7.2020 =#
using LinearAlgebra

function state(N)
    global sta_bas = []
    for n in 0:2^N-1
        sta_ba = BitArray(digits(n, base = 2, pad = N))
        push!(sta_bas,sta_ba)
    end
end
function count_up(sta)
    global u_n = 0
    for u in sta[:]
        if u
            u_n +=1
        end
    end
end
function block_state(N)
    for up in 0:N
        a = 0
        temp_sta =[]
        for s in 1:2^N
            count_up(sta_bas[s])
            if up == u_n
                a = a + 1
                push!(temp_sta,sta_bas[s])
            end
        end
        push!(M, a)
        block_stas[up+1] = temp_sta
        block_stas[up+1] = temp_sta
    end
end
#= function bitarr_to_int(arr) #let the Arrayto the Int number.
    return sum(arr .* (2 .^ collect(0:1:length(arr)-1)))
end =#
#= function findstate(S, a)  #still had some ting wong!!!!!!!
    global b = 0
    b_min = 1;b_max = m
    while true
        b = b_min + (b_max-b_min)*0.5
        b = Int(round(b, digits=0))
        if S[a] < S[b]#bool can not just so easy to compare eachother.!
            b_max = b - 1
        elseif S[a] > S[b]
            b_min = b + 1
        else
            break
        end
    end
end =#

function flip(S, a, i, j)
    st_rv = Dict{BitArray, Int64}()
    for nnn in 1:m
        nn = S[nnn]#cut extra part
        st_rv[nn] = (nnn)
    end
    global b = 0
    S[a][i] = ~S[a][i]
    S[a][j] = ~S[a][j]
    b = st_rv[S[a]]
    S[a][i] = ~S[a][i]
    S[a][j] = ~S[a][j]
end
function block_H(N,M)
    for n in 1:N+1
        global m = M[n]
        build_H(n, m)
    end
end
function build_H(n, m)
    h = zeros(m, m)
    for a in 1:m
        for i in 1:N
            j = mod1(i+1, N)
            if (block_stas[n][a][i] == block_stas[n][a][j])
                h[a,a] = h[a,a] + 0.25
                else
                    h[a,a] = h[a,a] - 0.25
                    flip(block_stas[n], a, i, j)
                    h[a,b] = 0.5
            end
        end
    end
    push!(H, h)
end

global N = 3
println("The length of Heisenbreg chain:", N)
global M = []
state(N)
global block_stas = Vector{Array}(undef, N+1)
block_state(N)
global H = []
block_H(N,M)
# show(stdout, "text/plain", H);println()
for i in 1:N+1
    println("###############    The blocks are:", i,"    ###############")
    E = eigen(H[i])
    #= println("Eigenvalues:")
    show(stdout, "text/plain", E.values);println()
    println("Eigenvectors:")
    show(stdout, "text/plain", E.vectors);println() =#
end