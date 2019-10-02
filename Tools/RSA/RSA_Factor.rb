#Algorithm to check for factors.  First checks 2,3,5 then increments by 30.
def factorize(n)
  if n%2==0 then return 2 end
  if n%3==0 then return 3 end
  if n%5==0 then return 5 end
  m = Math.sqrt(n)
  i=7
  while i<=m do
    if (n%i==0)      then return i end
    if (n%(i+4)==0)  then return i+4 end
    if (n%(i+6)==0)  then return i+6 end
    if (n%(i+10)==0) then return i+10 end
    if (n%(i+12)==0) then return i+12 end
    if (n%(i+16)==0) then return i+16 end
    if (n%(i+22)==0) then return i+22 end
    if (n%(i+24)==0) then return i+24 end
    i+=30
  end
end

#Factorize n
factorize(2531257) 

require 'openssl'
require 'base64'
a = OpenSSL::PKey::RSA::new
a.e = 43
a.n = 2531257
a.p = 509
a.q = a.n.to_i / a.p.to_i
a.d = a.e.mod_inverse((a.p-1) * (a.q-1))
a.dmp1 = a.d % (a.p-1)
a.dmq1 = a.d % (a.q-1)
a.iqmp = a.q.mod_inverse(a.p)
File.write('small.pem', a)


$ irb
require 'base64'
def nthroot(n, a, precision = 1e-1024)
  x = a
  begin
    prev = x
    x = ((n - 1) * prev + a / (prev ** (n - 1))) / n
  end while (prev - x).abs precision
 x
end
a = Base64.decode64("MCQCAQACAyafuQIBKwIDAOVzAgITbQICAf0CAg/PAgIBPwICEBs=")
a = a.unpack('H*')[0].to_i(16)
r = nthroot(3, a)
puts [r.to_s(16)].pack('H*')
hello