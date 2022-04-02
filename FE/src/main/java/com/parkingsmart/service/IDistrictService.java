package com.parkingsmart.service;

import java.util.List;

import com.parkingsmart.dto.DistrictDTO;

public interface IDistrictService {
	
	
	public List<DistrictDTO> findByIdProvince(String id);
	public DistrictDTO findById(String id);

}
