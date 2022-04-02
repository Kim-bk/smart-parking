package com.parkingsmart.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.parkingsmart.dto.DistrictDTO;
import com.parkingsmart.dto.ProvinceDTO;
import com.parkingsmart.entity.DistrictEntity;
import com.parkingsmart.mapper.DistrictMapper;
import com.parkingsmart.mapper.ProvinceMapper;
import com.parkingsmart.repository.DistrictRepository;
import com.parkingsmart.service.IDistrictService;

@Service
public class DistrictService implements IDistrictService{

	@Autowired
	private DistrictRepository repository;
	
	@Autowired
	private DistrictMapper mapper;
	
	@Autowired
	private ProvinceService provinceService;
	
	@Autowired
	private ProvinceMapper provinceMapper;
	
	@Override
	public List<DistrictDTO> findByIdProvince(String id) {
		List<DistrictDTO> list = new ArrayList<DistrictDTO>();
		ProvinceDTO province = provinceService.findOneById(id);
		if (province!=null) {
			List<DistrictEntity> districts = repository.findByProvince(provinceMapper.ToEntity(province));
			for (DistrictEntity item:districts) {
				list.add(mapper.toDTO(item));
			}
			return list;
		}
		
		return null;
	}

	@Override
	public DistrictDTO findById(String id) {
		Optional<DistrictEntity> entity = repository.findById(id);
		if (entity.isPresent()) {
			DistrictDTO district = mapper.toDTO(entity.get());
			return district;
		}
		return null;
	}

}
